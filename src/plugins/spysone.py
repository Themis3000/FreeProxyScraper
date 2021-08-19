import re
from bs4 import BeautifulSoup
from src.utils import Proxy, Plugin, get_soup
from typing import Iterator, Dict


# Spysone encodes the ports for their proxies in a very strange, complex way. All code before the class is part of the
# decoding process

def from_char_code(num: int) -> str:
    x = num.to_bytes(2, 'little')
    return x.decode('UTF-16')


def base36encode(number: int) -> str:
    alphabet, base36 = ['0123456789abcdefghijklmnopqrstuvwxyz', '']

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


# Don't even try to comprehend this, it's a waste of time. I don't understand what it does either. It's just a python
# version of some js found on the website I ripped and translated. All I know is this takes a few inputs, and then
# somehow turns the output into valid js code
def decoder(p, r, o, x, y, s) -> str:
    def y(c):
        val1 = "" if c < r else y(int(c / r))
        c = c % r
        val2 = from_char_code(c + 29) if c > 35 else base36encode(c)
        return val1 + val2

    while o > 0:
        o -= 1
        s[y(o)] = x[o] if x[o] != "" else y(o)

    o = 1

    while o > 0:
        o -= 1
        p = re.sub(r'\b\w+\b', lambda x: s[x.group()], p)
    return p


# Converts the decoded js code to a dictionary of values
def convert_decode(script: str) -> Dict[str, int]:
    pre_computed = script.split(";")[:-1]
    values = {}
    while len(pre_computed) != len(values):
        for entry in pre_computed:
            key, value = entry.split("=")

            # Handles for when already computed
            if key in values:
                continue

            # Handles for when value is a operation
            if "^" in value:
                power_values = value.split("^")

                # Handles for when operation is numeric
                if power_values[0].isnumeric():
                    values[key] = int(power_values[0]) ^ int(power_values[1])
                    continue

                # Handles when operation uses words and we have computed both values already
                if (power_values[0] and power_values[1]) in values:
                    values[key] = values[power_values[0]] ^ values[power_values[1]]
                continue

            values[key] = int(value)
    return values


# Process script that injects the port number into the dom
def process_script(script: str, values: Dict[str, int]) -> int:
    output = ""
    trimmed_script = script[20:-2]
    operations = trimmed_script.split(")+(")

    for operation in operations:
        names = operation.split("^")
        output += str(values[names[0]] ^ values[names[1]])

    return int(output)


# uses decoder and converts js decoder to retrieve values
def process_decode_str(decoder_str: str) -> Dict[str, int]:
    # Sanitized decoder of the actual function, leaving just the parameters. Removes any quotes from parameters
    params = decoder_str[329:-24].replace("'", "").split(",")
    decode = decoder(params[0],
                     60,
                     60,
                     params[3].split('\u005e'),
                     0,
                     {})
    return convert_decode(decode)


anon_dict = {"HIA": 2, "ANM": 1, "NOA": 0}


class Spysone(Plugin):
    plugin_name = "spysone"
    plugin_url = "https://spys.one/en/"

    def find(self) -> Iterator[Proxy]:
        status_code, soup = get_soup("https://spys.one/en/")

        if status_code != 200:
            self.report_fail()
            return

        script_string = soup.select_one("body > script").string
        values = process_decode_str(script_string)

        for element in soup.select("tr.spy1x[onmouseover],tr.spy1xx[onmouseover]"):
            entries = element.findChildren(recursive=False)
            port_coded = entries[0].font.script.string
            yield Proxy(
                ip=entries[0].text.strip(),
                port=process_script(port_coded, values),
                protocol=entries[1].text.lower(),
                anon_level=anon_dict[entries[2].text],
                country=entries[3].text
            )

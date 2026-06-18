import json

#open json file
with open("sample_data.json", "r") as file:
    data = json.load(file)

#print table header
print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 80)

#parse and print data
for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs["dn"]
    descr = attrs["descr"]
    speed = attrs["speed"]
    mtu = attrs["mtu"]

    print(f"{dn:50} {descr:20} {speed:8} {mtu:6}")
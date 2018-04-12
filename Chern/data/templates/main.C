# Please write the main file for this algorithm
# A demo is:
from arguments import parameters
from arguments import outputs

with open("{}/data.txt".format(outputs["txt_file"])) as f:
    n = parameters["n"]
    for i in range(n):
        f.write("".format(i))

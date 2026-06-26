import re

#exercise 1, a followed by zero or more b
text = "abbb"
print(re.match(r"ab*", text))

#exercise 2, a followed by 2 - 3 b
print(re.match(r"ab{2,3}", "abbb"))

#exercise 3, lowercase letters joined with underscore
text = "hello_world"
print(re.findall(r"[a-z]+_[a-z]+", text))

#exercise 4, uppercase followed by lowercase
text = "Hello World"
print(re.findall(r"[A-Z][a-z]+", text))

#exercise 5, a followed by anything ending b
print(re.match(r"a.*b", "axyzb"))

#exercise 6, replace spaces commas dots
text = "Hello, world. Python"
print(re.sub(r"[ ,.]", ":", text))

#exercise 7, snake case to camel case
text = "hello_world"
print(
    re.sub(
        r"_([a-z])",
        lambda x: x.group(1).upper(),
        text
    )
)

#exercise 8, split at uppercase
text = "HelloWorldPython"
print(
    re.split(r"(?=[A-Z])", text)
)

#exercise 9, add spaces before capitals
text = "HelloWorld"
print(
    re.sub(
        r"([A-Z])",
        r" \1",
        text
    )
)

#exercise 10, camel case to snake case
text = "helloWorld"
print(
    re.sub(
        r"([A-Z])",
        r"_\1",
        text
    ).lower()
)
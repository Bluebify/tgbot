import log

import sys, os

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def divide(item: list, col):
	returning = []
	breaking_index = []

	index = 0
	while index <= len(item):
		if index % col == 0:
			breaking_index.append(index - 1)
		index += 1

	breaking_index.pop(0)
	breaking_index.append(item[-1])

	print(breaking_index)
	r1 = []
	for i in range(len(item)):

		if i in breaking_index:
			r1.append(item[i])
			returning.append(r1)
			r1 = []

		else:
			r1.append(item[i])
	
	x = len(item)
	last_row = item[breaking_index[-2]:x]
	returning.append(last_row[1:])
	if returning[-1] == []:
		returning.pop()
		
	return returning


def gen_help_keyboard(plugin_list, col=3):
	keyboard = []
	for i in plugin_list:
		button = InlineKeyboardButton(i, callback_data=f"help_{i}")
		keyboard.append(button)
		
	x = divide(keyboard, col)
	return x

def list_all_modules() -> list:
    modules_directory = "ztgbot/plugins"

    all_modules = []
    for module_name in os.listdir(modules_directory):
        path = modules_directory + "/" + module_name

        if "__init__" in path or "__pycache__" in path or "log" in path:
            continue

        if path in all_modules:
            log.path("Modules with same name can't exists!")
            sys.exit(5)

        # One file module type
        if path.endswith(".py"):
            # TODO: removesuffix
            all_modules.append(module_name.split(".py")[0])

        # Module directory
        if os.path.isdir(path) and os.path.exists(path + "/__init__.py"):
            all_modules.append(module_name)

    return all_modules

ALL_MODULES = sorted(list_all_modules())
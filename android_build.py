import sys
import os
import commander
import utils
from logger import L
import gv
from time import sleep
from parse import Parser
import subprocess


def gen_key(args):
    store_file = gv.build_android_store_file()
    store_pass = gv.build_android_store_pass()
    alias_name = gv.build_android_alias_name()
    alias_pass = gv.build_android_alias_pass()
    name = gv.build_android_name_first_last_name()
    organizational_unit = gv.build_android_name_organizational_unit()
    organization = gv.build_android_name_organization()
    city = gv.build_android_name_city()
    state = gv.build_android_name_state()
    code_country = gv.build_android_name_code_country()

    if os.path.isfile(store_file):
        os.remove(store_file)
    cmd = 'keytool -genkey -v ' \
          '-keystore {0} ' \
          '-storepass {1} ' \
          '-alias {2} ' \
          '-keypass {3} ' \
          '-dname "CN={4}, OU={5}, O={6}, L={7}, ST={8}, C={9}" ' \
          '-keyalg RSA -keysize 2048 -validity 10000'
          # ' -deststoretype keystore'
    cmd = cmd.format(
        store_file,
        store_pass,
        alias_name,
        alias_pass,
        name,
        organizational_unit,
        organization,
        city,
        state,
        code_country
    )
    print(cmd)
    # cmd = 'keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000'
    os.system(cmd)
    # p = subprocess.Popen([cmd], shell=True,
    #                      stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #
    # params = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n".format(
    #     name,
    #     organizational_unit,
    #     organization,
    #     city,
    #     state,
    #     code_country,
    #     check,
    #     alias_pass,
    #     alias_pass)
    # print(params)
    #
    # p.stdin.write(params.encode('utf-8'))
    # # p.stdin.write(name.encode('utf-8'))
    # # p.stdin.write(organizational_unit.encode('utf-8'))
    # # p.stdin.write(organization.encode('utf-8'))
    # # p.stdin.write(city.encode('utf-8'))
    # # p.stdin.write(state.encode('utf-8'))
    # # p.stdin.write(code_country.encode('utf-8'))
    # # p.stdin.write(check.encode('utf-8'))
    # # p.stdin.write(alias_pass.encode('utf-8'))
    # # p.stdin.write(alias_pass.encode('utf-8'))
    # stdout, stderr = p.communicate()
    # print(stdout)
    # # stdout, stderr = p.communicate()
    # # print(stdout)
    pass


def gen_hash(args):
    mode = ""
    if len(args) > 0:
        parser = Parser(prog=utils.abs_path('./android_build.py'))
        parser.add_argument("-m", "--mode", default=mode, help="gen_hash() failed! |help: -m release|debug")
        arguments = parser.parse_args(args)
        mode = arguments.mode

    if mode == "debug":
        return _gen_hash_debug()
    if mode == "release":
        return _gen_hash_release()
    L.error("gen_hash() failed! |help: -m release|debug")


def _gen_hash_debug():
    # store_file = '~/.android/debug.keystore'
    # alias_pass = 'androiddebugkey'
    # cmd = "keytool -exportcert -alias {0} -keystore {1} -storepass {2}"
    # cmd = cmd.format(alias_pass, store_file)
    cmd = "keytool -exportcert -alias androiddebugkey -keypass android -storepass android -keystore ~/.android/debug.keystore | openssl sha1 -binary | openssl base64"

    print(cmd)
    os.system(cmd)
    pass


def _gen_hash_release():
    store_file = gv.build_android_store_file()
    if os.path.isfile(store_file):
        alias_name = gv.build_android_alias_name()
        alias_pass = gv.build_android_alias_pass()
        store_pass = gv.build_android_store_pass()
        cmd = "keytool -exportcert " \
              "-alias {0} " \
              "-keystore {1} " \
              "-keypass {2} " \
              "-storepass {3} " \
              "| openssl sha1 -binary | openssl base64"
        cmd = cmd.format(
            alias_name,
            store_file,
            alias_pass,
            store_pass)
        print(cmd)
        os.system(cmd)
    else:
        L.error("miss file keystore:" + store_file)


def main(args):
    gen = ""
    if len(args) > 1:
        parser = Parser(prog=utils.abs_path('./android_build.py'))
        parser.add_argument("-g", "--gen", default=gen, help="gen() failed! |help: -g keystore|hash")
        arguments = [args.pop(0), args.pop(0)]
        arguments = parser.parse_args(arguments)
        gen = arguments.gen

    if gen == "keystore":
        gen_key(args)
    elif gen == "hash":
        gen_hash(args)
    else:
        L.error("failed! |help: android-gen -g keystore|hash")


if __name__ == "__main__":
    args = utils.get_args(sys.argv)
    main(args)

#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

import json
import uhashlib
import ubinascii
import gc
import os
import machine

import config
import tankful
import urequests as requests

# Try to get version number
try:
    from OTA_VERSION import VERSION
except ImportError:
    VERSION = '0.0.1'


class OTA():
    # The following two methods need to be implemented in a subclass for the
    # specific transport mechanism e.g. WiFi

    def connect(self):
        tankful.connect()

    def get_data(self, req, dest_path=None):
        response = requests.get(self.url(req))

        if response is not None:
            if dest_path is not None:
                file = open(dest_path, 'w')
                file.write(response.text)
                file.close()

            file_content = response.text

            hash = uhashlib.sha1()
            hash.update(file_content)
            file_hash = ubinascii.hexlify(hash.digest()).decode()

            gc.collect()
            return file_content, file_hash


    def url(self, uri):
        import re
        uri = '/' + re.match(r'^\/?(.+)', uri).group(1)

        return config.update_base_url + uri

    # OTA methods

    def get_current_version(self):
        return VERSION

    def get_update_manifest(self):
        req = "/manifest.json?current_ver={}".format(self.get_current_version())
        print(req)
        response = requests.get(
            self.url('/manifest.json'),
            params={'current_ver':self.get_current_version()}
        )

        try:
            manifest = json.loads(response.text)
        except:
            manifest = None
            pass

        gc.collect()
        return manifest, response

    def update(self):
        print('Check for new firmware version...')
        manifest, response = self.get_update_manifest()

        print(manifest)

        if manifest is None:
            print("Already on the latest version")
            return response

        if 'current_ver' in manifest:
            print(manifest['current_ver'][0])
            return response

        print('Updating to version {}...'.format(manifest['version']))

        if 'new' in manifest and 'update' in manifest:
            # Download new files and verify hashes
            for f in manifest['new'] + manifest['update']:
                # Upto 5 retries
                for _ in range(5):
                    try:
                        self.get_file(f)
                        break
                    except Exception as e:
                        print(e)
                        msg = "Error downloading `{}` retrying..."
                        print(msg.format(f['URL']))
                else:
                    raise Exception("Failed to download `{}`".format(f['URL']))

            # Backup old files
            # only once all files have been successfully downloaded
            for f in manifest['update']:
                self.backup_file(f)

            # Rename new files to proper name
            for f in manifest['new'] + manifest['update']:
                new_path = "{}.new".format(f['dest_path'])
                dest_path = "{}".format(f['dest_path'])

                # make sure desitnation path is free first
                try:
                    self.delete_file(dest_path)
                except:
                    # probably doesn't exist
                    print('Faied to delete {}'.format(dest_path))
                    pass

                # rename
                try:
                    os.rename(new_path, dest_path)
                    print('Done: {}'.format(dest_path))
                except:
                    print('Failed to rename {} to {}'.format(new_path, dest_path))

        else:
            print('invalid manifest')
            print(manifest)

        if 'delete' in manifest:
            # `Delete` files no longer required
            # This actually makes a backup of the files incase we need to roll back
            for f in manifest['delete']:
                self.delete_file(f)
                print('Deleted: {}'.format(f))

        # Flash firmware
        if "firmware" in manifest:
            self.write_firmware(manifest['firmware'])

        # Save version number file
        try:
            self.backup_file({"dest_path": "/flash/OTA_VERSION.py"})
        except OSError:
            pass  # There isnt a previous file to backup

        with open("/flash/OTA_VERSION.py", 'w') as fp:
            fp.write("VERSION = '{}'".format(manifest['version']))
            print('new version: {}'.format(manifest['version']))

        from OTA_VERSION import VERSION

        print('Firmware now at version {}'.format(manifest['version']))
        print('Restarting...')

        # Reboot the device to run the new decode
        machine.reset()

    def get_file(self, f):
        new_path = "{}.new".format(f['dest_path'])

        # If a .new file exists from a previously failed update delete it
        try:
            os.remove(new_path)
        except OSError:
            pass  # The file didnt exist

        # Download new file with a .new extension to not overwrite the existing
        # file until the hash is verified.
        hash = self.get_data(f['URL'].split("/", 3)[-1], dest_path=new_path)[1]

        # Hash mismatch
        if hash != f['hash']:
            msg = "Downloaded file's hash does not match expected hash"
            print(hash)
            print(f['hash'])
            raise Exception(msg)

    def backup_file(self, f):
        bak_path = "{}.bak".format(f['dest_path'])
        dest_path = "{}".format(f['dest_path'])

        # Delete previous backup if it exists
        try:
            os.remove(bak_path)
        except OSError:
            pass  # There isnt a previous backup

        # Backup current file
        try:
            os.rename(dest_path, bak_path)
        except:
            pass

    def delete_file(self, f):
        bak_path = "/{}.bak_del".format(f)
        dest_path = "/{}".format(f)

        # Delete previous delete backup if it exists
        try:
            os.remove(bak_path)
        except OSError:
            pass  # There isnt a previous delete backup

        # Backup current file
        try:
            os.rename(dest_path, bak_path)
        except:
            pass

    def write_firmware(self, f):
        hash = self.get_data(f['URL'].split("/", 3)[-1])
        # TODO: Add verification when released in future firmware

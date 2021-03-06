#!/usr/bin/env python
import sys
import os


class LogParser:
    def __init__(self, log_file_path, target_directory, action_group):
        self.log_file_path = log_file_path
        self.target_directory = target_directory
        self.action_group = action_group
        self.timestamps = []
        self.__parse()
        self.__write_results()

    def __verify_action(self, action):
        right_part_group_identifier = action.split("actionGroupIdentifier='")[1]
        action_group_identifier = right_part_group_identifier.split("'")[0]
        return action_group_identifier == self.action_group

    @staticmethod
    def extract_error_id(action):
        return action.split("id=")[1].split(",")[0]

    def __parse(self):
        need_to_check_timestamp_1 = False
        need_to_check_timestamp_2 = False
        need_to_check_action_1 = False
        need_to_check_action_2 = False
        timestamps = []
        tmp_timestamp = None
        id_dict = {}
        with open(self.log_file_path) as f:
            for line in f:
                if "@@PRE_TIMESTAMP@@" in line:
                    need_to_check_timestamp_1 = True
                elif need_to_check_timestamp_1 is True:
                    need_to_check_timestamp_2 = True
                    need_to_check_timestamp_1 = False
                elif need_to_check_timestamp_2 is True:
                    tmp_timestamp = line.split("INFORMAZIONI: ")[1]
                    need_to_check_timestamp_2 = False
                elif "@@ACTION@@" in line:
                    need_to_check_action_1 = True
                elif need_to_check_action_1 is True:
                    need_to_check_action_2 = True
                    need_to_check_action_1 = False
                elif need_to_check_action_2 is True:
                    action_line = line.split("INFORMAZIONI: ")[1]
                    if self.__verify_action(action_line) is True:
                        id = self.extract_error_id(action_line)
                        if id_dict.get(id) is None:
                            id_dict[id] = True
                            timestamps.append(tmp_timestamp[:len(tmp_timestamp) - 1])
                    need_to_check_action_2 = False
        self.timestamps = timestamps

    def __write_results(self):
        with open(os.path.basename(self.log_file_path) + "_err_timestamps.txt", "w") as f:
            f.writelines(self.timestamps)


def main():
    args = sys.argv
    argc = len(args)
    if argc != 4:
        print("SCRIPT USAGE: [LOG_FILE_PATH] [TARGET_DIRECTORY] [ACTION_GROUP_FOR_ERRORS]")
        exit(-1)
    else:
        if os.path.isfile(args[1]) is False:
            print("PLEASE PROVIDE A VALID LOG_FILE_PATH")
            exit(-1)
        if os.path.isdir(args[2]) is False:
            print("PLEASE PROVIDE A VALID TARGET DIRECTORY FOR THE ERROR TIMESTAMPS")
            exit(-1)
        if args[3] == "":
            print("PLEASE PROVIDE A VALID ACTION_GROUP FOR ERRORS")
            exit(-1)
        LogParser(args[1], args[2], args[3])


if __name__ == "__main__":
    main()

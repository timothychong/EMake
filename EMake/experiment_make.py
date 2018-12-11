import os
import errno
import copy
from shutil import copy2

def pjoin(a, b):
    if a.endswith('/'):
        return a + b
    return a + '/' + b

def mkdir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

dir_path = os.path.dirname(os.path.realpath(__file__))

class ExperimentMake(object):

    # support files
    support_folder = "make-util"
    run_file = "run.sh"
    support_run = pjoin(support_folder, run_file)

    #makefile = "Makefile-run"
    #output_folder = "output"
    folder_prefix = "f_"
    my_targets = None
    _flattened_targets = None
    _str_flattened_targets = None
    _str_flattened_folders = None


    def __init__(self):
        self.my_targets = self.targets()

    def validate(self):
        assert self.makefile
        assert self.output_folder

    def targets(self):
        # Return a dict/list of targets
        assert self.my_targets
        return self.my_targets

    def dict_sort(self, d):
        return (d[0], d[1])

    def traverse_targets(self, obj):
        assert(obj)
        if isinstance(obj, list):
            for o in obj:
                assert not (isinstance(o, list) or isinstance(o, dict))
                yield o

        elif isinstance(obj, dict):
            for k, v in sorted(obj.iteritems(), key=self.dict_sort):
                out_ini = [k]

                for i in self.traverse_targets(v):
                    out = copy.deepcopy(out_ini)
                    if isinstance(v, dict):
                        out.extend(i)
                    else:
                        out.append(i)
                    yield out

        else:
            yield obj


    def flattened_targets(self):
        if self._flattened_targets:
            return self._flattened_targets
        out = []
        for i in self.traverse_targets(self.my_targets):
            out.append(i)
        self._flattened_targets = out
        return out

    def str_flattened_targets(self):
        if self._str_flattened_targets:
            return self._str_flattened_targets

        out = []
        for i in self.traverse_targets(self.my_targets):
            if isinstance(i, list):
                out.append("_".join([ (str(j[0]) if isinstance(j, tuple) else str(j)) for j in i]))
            elif isinstance(i, tuple):
                # IF tuple, just use the first item
                out.append(str(i[0]))
            else:
                out.append(str(i))

        self._str_flattened_targets = out
        return out

    def str_flattened_targets_folder(self):
        if self._str_flattened_folders:
            return self._str_flattened_folders

        out = [pjoin(self.output_folder, self.folder_prefix +
               x) for x in self.str_flattened_targets()]
        self._str_flattened_folders = out
        return out

    def run_setup(self, rundir, pwd, params):
        # Does things to set up directory to run
        assert(False and "Run setup Need to be customized")

    def run_command(self, rundir, pwd, params):
        # Return the string that it uses to run in the Make file
        assert(False and "Run Command Need to be customized")

    def replace_template(self, template, target, params):
        with open(template, 'r') as handle:
            s = handle.read()

        for key, value in params.iteritems():
            s = s.replace(key, value)

        with open(target, 'w') as handle:
            handle.write(s)

    def setup_folders(self):
        class_name = self.__class__.__name__
        mkdir(self.output_folder)
        for folder in self.str_flattened_targets_folder():
            mkdir(folder)
        for result in self.gather_result():
            mkdir("{}_{}".format(class_name, result[0]))

        self.str_flattened_targets_folder()

    def run_setup_all(self):
        assert self._str_flattened_folders and "Folders are not setup before being used"
        index = 0
        oldcwd = os.getcwd()
        # print self.flattened_targets()
        for target in self.flattened_targets():
            folder_path = pjoin(oldcwd, self._str_flattened_folders[index])

            # Go to every target folder and run set up
            os.chdir(folder_path)

            self.run_setup( oldcwd, folder_path , target)

            # copying support files
            copy2(pjoin(dir_path, self.support_run), folder_path)

            with open("command.sh", "w+") as handle:
                handle.write(self.run_command(oldcwd, folder_path, target))

            os.chdir(oldcwd)
            index += 1

    def gather_result(self):
        # Return a list of files that you want to gather
        # tuples of file and extensions
        assert(False and "gather result Need to be customized")


    def gen_make(self):

        out_str = ""
        class_name = self.__class__.__name__
        out_str += "# Auto generated Makefile for {}\n".format(class_name)

        # All targets
        done_file = "done"

        out_str += "SHELL = /bin/bash\n"

        out_str += "all: "

        # clear lock
        out_str += "clear_lock "

        for result in self.gather_result():
            for i, target in enumerate(self._str_flattened_folders):
                out_str += "{} ".format(pjoin(class_name + '_' + result[0], self._str_flattened_targets[i]+ result[1]))

        target_str = " ".join([pjoin(x, done_file) for x in self.str_flattened_targets_folder()])
        out_str += "{} ".format(target_str)

        out_str += "\n\n"

        # clear_lock target
        out_str += "clear_lock:\n"
        out_str += "\tfind {} -name \"lock_`hostname`\" | xargs -r rm\n\n".format(self.output_folder)


        for target in self.str_flattened_targets_folder():
            out_str += "{}: | clear_lock\n".format(pjoin(target, done_file))
            out_str += "\t\tpushd {} && bash {} && popd\n\n".format(target, self.run_file)

        # Gather results at the end
        # out_str += "gather_result: {}\n".format(target_str)

        assert self._str_flattened_targets
        assert self._str_flattened_folders

        for result in self.gather_result():
            for i, target in enumerate(self._str_flattened_folders):
                out_str += "{}: {}\n".format(pjoin(class_name + '_' + result[0], self._str_flattened_targets[i]+ result[1]), pjoin(target, done_file))
                out_str += "\tif [ -a {} ];\\\n".format(pjoin(target, result[0]))
                out_str += "\tthen \\\n"
                out_str += "\t\tcp {} {}; \\\n".format(pjoin(target, result[0]), pjoin(class_name + '_' + result[0], self._str_flattened_targets[i]+ result[1]))
                out_str += "\tfi;\n"
            out_str += "\n"

        with open(self.makefile, "w") as handle:
            handle.write(out_str)

# if __name__ == "__main__":
    # main()


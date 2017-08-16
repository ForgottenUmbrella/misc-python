import sys
import inspect
import logging
from random import randint


def experimental_probability(test, trials=100):
    print("Experiment: {}".format(test.__name__))
    print("Event: {}".format(inspect.getdoc(test)))
    print("Number of trials: {}".format(trials))
    print()

    def exp_test(*args):
        for x, arg in enumerate(inspect.getargspec(test)[0]):
            print("{}: {}".format(arg, args[x]))
        print("Girls do their best now and are preparing. "
              "Please wait warmly until it is ready.")
        num_occurrence = 0
        for __ in range(trials):
            if test(*args):
                num_occurrence += 1
        print("Experimental probability of {}% ({} out of {} time{})".format(
            num_occurrence*100 // trials, num_occurrence, trials,
            "s" if trials != 1 else ""))
        print()

    return exp_test


def same_bday(num_people):
    """A person in a theoretical room of 'num_people' people has the same
    birthday as another.
    """
    bdays = [randint(1, 365) for __ in range(num_people)]
    logging.info("bdays list: {}".format(bdays))
    for i, bday_1 in enumerate(bdays[:-1]):
        logging.debug("Iteration {}:\n".format(i))
        # Will only iterate until a match is found
        logging.debug("bday to compare: {}".format(bday_1))
        for j, bday_2 in enumerate(bdays[i+1 :]):
            logging.debug("{}: same as {}? {}".format(
                i+1+j, bday_2, bday_1 == bday_2))
            if bday_1 == bday_2:
                logging.info("Found match after iteration {}.\n".format(i))
                return True
    return False


if __name__ == '__main__':
    level = getattr(logging, input(
        "Logging level (CRITICAL, ERROR, WARNING, INFO or DEBUG)? ").upper())
    experiment = globals().get(input("Experiment ({}): ".format(", ".join(
        [f.__name__ for f in [i[1] for i in inspect.getmembers(
        sys.modules[__name__])] if inspect.isfunction(f)][1:]))))
    print()

    while True:
        num_trials = int(input("Trial size: "))
        parameters = inspect.getargspec(experiment)[0]
        sample_space = int(input("Sample space ({}): ".format(parameters[0])))
        args = [input("{}: ".format(arg)) for arg in enumerate(parameters[1:])]

        logging.basicConfig(
            filename='experimental_probability.log', level=level)
        with open('experimental_probability.log', 'w'):
            # Clear log
            pass
        if args:
            experimental_probability(experiment, num_trials)(sample_space, args)
        else:
            experimental_probability(experiment, num_trials)(sample_space)
        print()
        if input("Quit? (True/False) ").capitalize() == "True":
            break


# exp_same_bday = experimental_probability(same_bday, 100)
# exp_same_bday(365)
# exp_same_bday(70)
# exp_same_bday(23)

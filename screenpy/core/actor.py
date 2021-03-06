import re


class Actor:

    def __init__(self, name):
        self.name = name
        self.abilities = dict()

    @classmethod
    def called(cls, name):
        return cls(name)

    def who_can(self, *args):
        for ability in args:
            ability_class_name = get_ability_class_name(ability)
            ability_name = convert_to_snake_case(ability_class_name)
            self.abilities[ability_name] = ability() if is_class(ability) else ability
        return self

    def can(self, do_something):
        ability_class_name = get_ability_class_name(do_something)
        return convert_to_snake_case(ability_class_name) in self.abilities

    def ability_to(self, do_something):
        if self.can(do_something):
            return self.abilities[convert_to_snake_case(get_ability_class_name(do_something))]
        else:
            raise AttributeError("{} doesn't have the ability to {}".format(self.name, get_ability_class_name(do_something)))

    def attempts_to(self, do_something):
        try:  # iterable? split out
            for something in do_something:
                self.attempts_to(something)
        except TypeError:  # not iterable
            if hasattr(do_something, 'interactions'):  # task? attempt interactions
                self.attempts_to(do_something.interactions)
            elif hasattr(do_something, 'perform_as'):  # interaction? perform it
                do_something.perform_as(self)
            else:
                raise TypeError("Actor tried to do something that was neither an iterable, "
                                "task object or interaction object. Object passed to attempts_to: {}"
                                .format(do_something))

    def sees(self, question):
        return question.answered_by(self)

    def __repr__(self):
        return "{}:{{ abilities: {}}}".format(self.name, self.abilities)


# grabbed from https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def convert_to_snake_case(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_ability_class_name(ability):
    return ability.__name__ if is_class(ability) else type(ability).__name__


def is_class(object):
    try:
        object.__name__
        return True
    except AttributeError:
        return False

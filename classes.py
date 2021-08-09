
class Card:

    def __init__(self, suit, value):
        self.suit = suit
        if value not in ['Jack', 'Queen', 'King', 'Ace']:
            self.pip_value = value
        else:
            setattr(self, 'face_card', value)
            self.pip_value = 11 if self.face_card == "Ace" else 10

    def __str__(self):
        return f"{self.face_card} of {self.suit}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.suit}, {self.face_card})"

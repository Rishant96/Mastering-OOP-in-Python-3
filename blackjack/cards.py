from functools import partial
import random
from abc import ABCMeta, abstractmethod 

class Suit:
	def __init__( self, name, symbol ):
		self.name = name
		self.symbol = symbol		
	def __str__( self ):
		return self.name + ": " + self.symbol

Club, Diamond, Heart, Spade = Suit('Club', '♣'), Suit('Diamond', '♦'), \
Suit('Heart', '♥'), Suit('Spade', '♠')	

class Card:
	def __init__( self, rank, suit ):
		self.suit = suit
		self.rank = rank
		self.hard, self.soft = self._points()
	def __str__( self ):
		return self.suit.symbol + ' ' + self.rank

class NumberCard( Card ):
	def _points( self ):
		return int(self.rank), int(self.rank)

class AceCard( Card ):
	def _points( self ):
		return 1, 11

class FaceCard( Card ):
	def _points( self ):
		return 10, 10

def card( rank, suit ):
	if rank == 1: return AceCard('A', suit)
	elif 2 <= rank < 11: return NumberCard( str(rank), suit )
	elif 11 <= rank < 14: 
		name = {11: "J", 12: "Q", 13: "K"}[rank]
		return FaceCard( name, suit )
	else:
		raise Exception( "Rank out of range" )

def card2( rank, suit ):
	if rank == 1: return AceCard('A', suit)
	elif 2 <= rank < 11: return NumberCard( str(rank), suit )
	else:
		name = { 11: 'J', 12: 'Q', 13: 'K' }[rank]
		return FaceCard( name, suit )

def card3( rank, suit ):
	if rank == 1: return AceCard( 'A', suit )
	elif 2 <= rank < 11: return NumberCard( str(rank), suit )
	elif rank == 11:
		return FaceCard( 'J', suit )
	elif rank == 12:
		return FaceCard( 'Q', suit )  
	elif rank == 13:
		return FaceCard( 'K', suit )
	else:
		raise Exception( "Rank out of range" )

def card4( rank, suit ):
	class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, NumberCard)
	return class_( rank, suit )

def card4_2( rank, suit ):
	class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, NumberCard)
	rank_str = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}.get(rank, str(rank))
	return class_(rank_str, suit)

def card4_3( rank, suit ):
	class_, rank_str = {
		1: (AceCard, 'A'),
		11: (FaceCard, 'J'),
		12: (FaceCard, 'Q'),
		13: (FaceCard, 'K'),
		}.get(rank, (NumberCard, str(rank)))
	return class_( rank_str, suit )


def card4_4( rank, suit ):
	part_class = {
		1: partial(AceCard, 'A'),
		11: partial(FaceCard, 'J'),
		12: partial(FaceCard, 'Q'),
		13: partial(FaceCard, 'K'),
		}.get(rank, partial(NumberCard, str(rank)))
	return part_class(suit)

deck = [card(rank, suit)
	for suit in (Club, Diamond, Heart, Spade)
		for rank in range(1,14)]

class Deck:
	def __init__( self ):
		self._cards = [card4_3(r,s) for s in (Club, Heart, 
				Diamond, Spade) for r in range(13)]
		random.shuffle( self._cards )
	def pop( self ):
		return self._cards.pop()

class Deck2( list ):
	def __init__( self ):
		super().__init__( card4_3(r+1,s) for r in range(13) for s 
		in (Club, Diamond, Heart, Spade) )
		random.shuffle( self )

class Deck3( list ):
	def __init__(self, decks=1):
		super().__init__()
		for i in range(decks):
			self.extend( card4_3(r+1,s) for r in range(13) for s in
			(Club, Diamond, Heart, Spade) )
		random.shuffle( self )
		burn = random.randint(1, 52)
		for i in range(burn) : self.pop()

class Hand:
	def __init__( self, dealer_card ):
		self.dealer_card = dealer_card
		self.cards = []
	def hard_total( self ):
		return sum(c.hard for c in self.cards)
	def soft_total( self ):
		return sum(c.soft for c in self.cards)

class Hand2:
	def __init__( self, dealer_card, *cards ):
		self.dealer_card = dealer_card
		self.cards = list(cards)
	def hard_total( self ):
		return sum(c.hard in self.cards)
	def soft_total( self ):
		return sum(c.soft in self.cards)

class Hand3:
	def __init__(self, *args, **kwargs):
		if len(args) == 1 and isinstance(args[0],Hand3):
			# Clone an existing hand; often a bad idea
			other = args[0]
			self.dealer_card = other.dealer_card
			self.cards = other.cards
		else:
			# Build a fresh, new hand.
			dealer_card, *cards = args
			sel.dealer_card = dealer_card
			self.cards = list(cards)

class Hand4:
	def __init__(self, *args, **kw):
		if len(args) == 1 and isinstance(args[0], Hand4):
			# Clone an existing hand often a bad idea
			other = args[0]
			self.dealer_card = other.dealer_card
			self.cards = other.cards
		elif len(args) == 2 and isinstance(args[0], Hand4) \
		and 'split' in kw:
			# Split an existing hand
			other, card = args
			self.dealer_card = other.dealer_card
			self.cards = [other.cards[kw['split']], card]
		elif len(args) == 3:
			# Build a fresh, new hand.
			dealer_card, *cards = args
			self.dealer_card = dealer_card
			self.cards = cards
		else:
			raise TypeError( "Invalid constructor args={0!r}"
				"kw={1!r}".format(args, kw) )

	def __str__(self):
		return ", ".join( map(str, self.cards) )

def Hand5:
	def __init__( self, dealer_card, *cards ):
		self.dealer_card = dealer_card
		self.cards = list(cards)
	@staticmethod
	def freeze( other ):
		hand = Hand5( other.dealer_card, *other.cards )
		return hand
	@staticmethod
	def split( other, card0, card1 ):
		hand0 = Hand5( other.dealer_card, other.cards[0], card0 )
		hand1 = Hand5( other.dealer_card, other.cards[1], card1 )
		return hand0, hand1
	def __str__( self ):
		return ", ".join( map(str, self.cards) )

class GameStrategy:
	def insurance( self, hand ):
		return False
	def split( self, hand ):
		return False
	def double( self, hand ):
		return False
	def hit( self, hand ):
		return sum(c.hard for c in hand.cards) <= 17

class Table:
	def __init__( self ):
		self.deck = Deck()
	def place_bet ( self, amount ):
		print( "Bet", amount )
	def get_hand( self ):
		try:
			self.hand = Hand2( d.pop(), d.pop(), d.pop() )
			self.hole_card = d.pop()
		except IndexError:
			# Out of cards: need to shuffle
			self.deck = Deck()
			return self.get_hand()
		print( "Deal", self.hand )
		return self.hand
	def can_insure( self, hand ):
		return hand.dealer_card.insure 

class BettingStrategy:
	def bet( self ):
		raise NotImplementedError( "No bet method" )
	def record_win( self ):
		pass
	def record_loss( self ):
		pass

class Flat(BettingStrategy):
	def bet( self ):
		return 1 

class BettingStrategy2(metaclass=ABCMeta):
	@abstractmethod
	def bet( self ):
		return 1
	def record_win( self ):
		pass
	def record_loss( self ):
		pass

class Player:
	def __init__( self, table, bet_strategy, game_strategy ):
		"""Creates a new player associated with a table,
		and configured with proper betting and play strategies

		:param table: an instance of the :class:'Table'
		:param bet_strategy: an instance of the :class:'BettingStrategy'
		:param game_strategy: an instance of :class:'GameStrategy'
		"""
		self.bet_strategy = bet_strategy
		self.game_strategy = game_strategy
		self.table = table
	def game( self ):
		self.table.place_bet( self.bet_strategy.bet() )
		self.hand = self.table.get_hand()
		if self.table.can_insure( self.hand ):
			if self.game_strategy.insurance( self.hand ):
				self.table.insure( self.bet_strategy.bet() )

class Player2:
	def __init__( self, **kwargs ):
		""" Must provide table, bet_strategy, game_strtegy. """
		self.__dict__.update( kw )
	def game( self ):
		self.table.place_bet( self.bet_strategy.bet() )
		self.hand = self.table.get_hand()
		if self.table.can_insure( self.hand ):
			if self.game_strategy.insurance( self.hand ):
				self.table.insure( self.bet_strategy.bet() )
	# etc.

class Player3:
	def __init__(self, table, bet_strategy, game_strategy, 
		**extras):
		self.bet_strategy = bet_strategy
		self.game_strategy = game_strategy
		self.table = table
		self.__dict__.update( extras )

class ValidPlayer:
	def __init__(self, table, bet_strategy, game_strategy):
		assert isinstance(table, Table)
		assert isinstance(bet_strategy, BettingStrategy)
		assert isinstance(game_strategy, GameStrategy)

		self.table = table
		self.game_strategy = game_strategy
		self.bet_strategy = bet_strategy 

if __name__ == '__main__':
	table = Table()
	flat_bet = Flat()
	dumb = GameStrategy()
	
	p = Player(table, flat_bet, dumb)
	p.game()

	p1 = Player2( table=table, bet_strategy=flat_bet, 
	game_strategy=dumb )
	p1.game()

	p2  Player2( table=table, bet_strategy=flat_bet, 
	game_strategy=dumb, log_name="Flat/Dumb" )
	p2.game()

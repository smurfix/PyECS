import unittest
import sys

# quick-n-dirty for debug only
sys.path.append('..')
import ecs

class ListTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def dump(self, list):
		print "ListId: ", list.ListId
		print "CustomerName: ", list.CustomerName
		print 

	def testListSearch(self):
		lists = ecs.ListSearch(ListType="WishList", City="Chicago", FirstName="Sam")
		self.assert_(len(lists) > 3)
		list = lists[0]
		self.assertNotEqual(list, None)
		# self.dump(list)
		self.assert_(list.CustomerName.find("Sam") > -1)

	def testListLookup(self):
		lists = ecs.ListLookup(ListType="WishList", ListId="13T2CWMCYJI9R")
		self.assertNotEqual(lists, None)
		self.assertEqual(lists[0].CustomerName, "Sam")

class QueryTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def dump(self, book):
		try:
			print "ASIN: ", book.ASIN
			print "Title : ", book.Title
			print "Author: ", book.Author
			print "Manufacturer: ", book.Manufacturer
			print 
		except :
			pass

	def testItemLookup(self):
		books = ecs.ItemLookup("0596009259")
		self.assertEqual(len(books), 1)
		book = books[0]
		self.assertNotEqual(book, None)

		self.assertEqual(book.ASIN, '0596009259')
		self.assertEqual(book.Title, 'Programming Python')
		self.assertEqual(book.Manufacturer, "O'Reilly Media, Inc.")
		self.assertEqual(book.ProductGroup, 'Book')
		self.assertEqual(book.Author, 'Mark Lutz')


	def testItemSearch(self):
		books = ecs.ItemSearch("", Title="Python", SearchIndex="Books")
		self.assert_(len(books) > 200, "We are expect more than 200 books are returned.")
		self.assertNotEqual(books[100], None)
	
	def testSimilarityLookup(self):
		books = ecs.SimilarityLookup("0596009259")
		#for book in books:
		#	self.dump(book)
		self.assert_(len(books) > 9, "We are expect more than 9 books are returned.")

class CartTest( unittest.TestCase ):
	def setUp(self):
		# prepare the python books to add 
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");
		self.books = ecs.ItemSearch("python", SearchIndex="Books")
		self.cart = None

	def testCartCreate(self):
		items = (self.books[0], self.books[1], self.books[2])
		qs = (1, 3, 5)

		self.cart = ecs.CartCreate(items, qs)
		for i in range(3):
			self.assertEqual(self.books[i].ASIN, self.cart.CartItems[i].ASIN)
			self.assertEqual(qs[i], int(self.cart.CartItems[i].Quantity))

	def testCartAdd(self):
		self.testCartCreate() 

		l = []
		for x in self.cart.CartItems:
			z = (x.ASIN, int(x.Quantity))
			l.append(z)
			
		items = (self.books[5], self.books[8])
		qs = (5, 8)
		z = (self.books[5].ASIN, 5)
		l.append(z)
		z = (self.books[8].ASIN, 8)
		l.append(z)

		self.cart = ecs.CartAdd(self.cart, items, qs)

		# check the item
		for item in self.cart.CartItems:
			self.assert_( (item.ASIN, int(item.Quantity)) in l)

	def testCartGet(self):
		self.testCartCreate() 

		cart = ecs.CartGet(self.cart)
		for i in range(len(cart.CartItems)):
			self.assertEqual(self.cart.CartItems[i].ASIN, cart.CartItems[i].ASIN)
			self.assertEqual(self.cart.CartItems[i].Quantity, cart.CartItems[i].Quantity)

	def testCartModify(self):
		self.testCartCreate()

		cart = ecs.CartModify(self.cart, (self.cart.CartItems[1], self.cart.CartItems[2]), (10, 'SaveForLater'))
		# Item 0 is the same
		self.assertEqual(self.cart.CartItems[0].Title, cart.CartItems[0].Title)
		self.assertEqual(self.cart.CartItems[0].Quantity, cart.CartItems[0].Quantity)
		# Item 1: Quantity is different
		self.assertEqual(self.cart.CartItems[1].Title, cart.CartItems[1].Title)
		self.assertEqual(10, int(cart.CartItems[1].Quantity))
		
		# Item 2: saved for later
		self.assertEqual(2, len(cart.CartItems))
		self.assertEqual(cart.SavedForLaterItems[0].Title, self.cart.CartItems[2].Title)
		self.assertEqual(cart.SavedForLaterItems[0].Quantity, self.cart.CartItems[2].Quantity)

	def testCartClear(self):
		self.testCartCreate()

		cart = ecs.CartModify(self.cart, (self.cart.CartItems[1], self.cart.CartItems[2]), (10, 'SaveForLater'))
		cart = ecs.CartClear(cart)
		self.failIf(hasattr(cart, 'CartItems'))
		self.failUnless(hasattr(cart, 'SavedForLaterItems'))

class SellerTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def testSellerLookup(self):
		# TODO: We need another SellerId here
		sellers = ecs.SellerLookup(['A3ENSIQ3ZA4FFN'])
		self.assertEqual(sellers[0].Nickname, 'abebooks')

class CustomerTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def testCustomerContentSearch(self):
		cs = ecs.CustomerContentSearch('Sam', None, 20)
		self.assertEqual(len(cs), 20)

class BrowseNodeLookupTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def testBrowserNodeLookup(self):
		bnl = ecs.BrowseNodeLookup('1065852')
		self.assertEqual(len(bnl), 1)
		self.assertEqual(bnl[0].Name, 'Plasma TVs')
		children = bnl[0].Children
		self.assertEqual(len(children), 2)

		self.assertEqual(children[0].BrowseNodeId, '13005341')
		self.assertEqual(children[1].BrowseNodeId, '11091111')

class HelpTest(unittest.TestCase):
	def setUp(self):
		ecs.setLicenseKey("1MGVS72Y8JF7EC7JDZG2");

	def testHelp(self):
		el = ecs.Help(HelpType="Operation", About="CartAdd")
		reference = {'AvailableParameters': ['AWSAccessKeyId', 'ContentType', 'LinkCode', 'Marketplace', 'MarketplaceDomain', 'MergeCart', 'Style', 'Validate', 'Version', 'XMLEscaping'],
			'AvailableResponseGroups': ['Request', 'Cart', 'CartSimilarities', 'CartTopSellers', 'CartNewReleases'], 
			'RequiredParameters': ['AssociateTag', 'CartId', 'HMAC', 'Items'], 
			'DefaultResponseGroups': ['Request', 'Cart'] }
		
		for x in ('AvailableParameters', 'AvailableResponseGroups', 
			'RequiredParameters', 'DefaultResponseGroups'):
			self.assertEqual(getattr(el.OperationInformation,x), reference[x])
				


		

if __name__ == "__main__" :
	unittest.main()


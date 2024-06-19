#=======Importing Libraries=======

#install tabulate module: pip install tabulate
from tabulate import tabulate
from operator import attrgetter


#========The beginning of the class==========
class Shoe:
    '''A class to represent a shoe.
    
    Attributes:
    -------
        country : str
        code : str
        product : str
        cost : int
        quantity : int
        
    Methods:
    -------
        get_cost()
        get_quantity()
        __str__()
    '''

    def __init__(self, country, code, product, cost, quantity):
        '''Constructs all the necessary attributes for the shoe object.
        
        Parameters:
        -------
            country : str
            code : str
            product : str
            cost : int
            quantity : int
        '''
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        
        
    def get_cost(self):
        '''Return the cost of the shoes.'''
        return int(self.cost)
        

    def get_quantity(self):
        '''Return the quantity of the shoes.'''
        return int(self.quantity)
    
    #needed to tablulate object
    def object_list(self):
        '''Return a list of the object attributes.'''
        obj_list = [self.country, self.code, self.product, self.cost, self.quantity]
        return obj_list


    def __str__(self):
        '''Return a string representation of the class.'''
        
        class_string = f'''
        Country: \t\t {self.country}
        Shoe code: \t\t {self.code}
        Product name: \t\t {self.product}
        Cost of product: \t {self.cost}
        Quantity of product: \t {self.quantity}
        '''
        return class_string


#=============Shoe list===========

#list to store shoe objects
shoe_list = []

#.txt file with shoe info
data = 'inventory.txt'


#==========Functions outside the class==============
def read_shoes_data(data,shoe_list):
    '''Open data file containing shoe information and read the data.
    Create a shoes object for each line in the data file.
    Append each shoes object to the shoe list.
    
    Parameters:
    -------
        data : .txt file
        shoe_list : list
        
    Returns:
    -------
        shoe_list : list
    '''
    
   
    index = 1
    #try to open the file
    try:
        with open(data, 'r+') as f:
            for line in f:
                #try to add shoe object from line
                try:
                    shoe_data = line.split(',')
                    shoe_object = Shoe(shoe_data[0],shoe_data[1],shoe_data[2],int(shoe_data[3]),int(shoe_data[4]))
                    shoe_list.append(shoe_object)
                except:
                    print(f"\nError adding line {index} of {data}.")
                index += 1
    except:
        print(f"\nError opening file {data}.")
    
    #delete first element with headers
    shoe_list.pop(0)
    
    return shoe_list
    
    
def capture_shoes(shoe_list):
    '''Create a shoe object from input obtained from user.
    Append shoe object to shoe list.
    
    Parameters:
    -------
        shoe_list : list
    
    Returns:
    -------
        shoe_list : list
    '''
    
    #get code of shoe from user
    code = input("\nPlease enter the code of the shoes: ")
    
    #check if product code already exists
    if any(shoe.code == code for shoe in shoe_list):  #code adapted from https://bobbyhadz.com/blog/python-find-object-in-list-of-objects#:~:text=%23%20Check%20if%20object%20exists%20in,list%2C%20otherwise%20False%20is%20returned.&text=Copied!,-class%20Employee()%3A
        print("\nThis product is already listed.")
    #if product does not exist, obtain other information from user
    else:
        country = input("\nPlease enter the country from which the shoes originate: ")
        product = input("\nPlease enter the product name: ")
        #make sure user input is an integer
        while True:
            try:
                cost = int(input("\nPlease enter the cost of the shoes: "))
                break
            except ValueError:
                print("\nInvalid input. Please try again.")
        while True:
            try:
                quantity = int(input("\nPlease enter the quantity of shoes: "))
                break
            except ValueError:
                print("\nInvalid input. Please try again.")
        #creat shoe object and append to shoe list
        shoe_object = Shoe(country,code,product,cost,quantity)
        shoe_list.append(shoe_object)
        
        shoe_str = "\n".join(",".join((shoe.country, shoe.code, shoe.product, str(shoe.cost), str(shoe.quantity))) for shoe in shoe_list) # adapted from https://stackoverflow.com/questions/43253916/python-string-join-multiple-attributes-from-object

        with open(data,'w+') as f:
            f.write(shoe_str)
        
        print(f"\n{product} added successfully.")
    
    return shoe_list
    
   
def view_all(shoe_list):
    '''Print a table of all the shoe objects'''
    
    #make a list of lists containing object attributes
    shoe_list_list = []
    for shoe in shoe_list:
        shoe_list_list.append(shoe.object_list())
    #tabulate and print information
    print()
    print(tabulate(shoe_list_list, headers = ['Country:','Code:','Product:','Cost:','Quantity:']))
   

def re_stock(shoe_list,data):
    '''Find shoe object with lowest quantity.
    Ask user if they'd like to restock.
    Update quantity of object on file.
    
    Parameters:
    -------
        shoe_list : list
        
    Returns:
    -------
        None
    '''
    #determine and print the shoe object with the minimum quantity
    lowest_stock = min(shoe_list, key=attrgetter('quantity')) #found at https://www.geeksforgeeks.org/python-get-the-object-with-the-max-attribute-value-in-a-list-of-objects/
    min_index = shoe_list.index(lowest_stock) #index of object in order to update attribute
    print(f"\nProduct with lowest stock: \t {lowest_stock.product}")
    
    #check if user would like to restock
    restock_quant = 0
    while True:
        restock = input("\nWould you like to restock this product? (Y?N): ")
        restock=restock.lower()
        #if yes, obtain quantity after restock
        if restock == 'y':
            while True:
                try:
                    restock_quant = int(input("\nPlease enter the quantity after restock: "))
                    break
                except ValueError:
                    print("\nInvalid input. Please try again.")
            break
        elif restock == 'n':
            break
        else:
            print("\nInvalid input. Please try again.")
    #if shoe has been restocked, update quantity and write to .txt file
    if restock_quant != 0:
        shoe_list[min_index].quantity = restock_quant
        
        shoe_str = "\n".join(",".join((shoe.country, shoe.code, shoe.product, str(shoe.cost), str(shoe.quantity))) for shoe in shoe_list) # adapted from https://stackoverflow.com/questions/43253916/python-string-join-multiple-attributes-from-object
        with open(data,'w+') as f:
            f.write(shoe_str)
            
    
def search_shoe(shoe_list):
    '''Search for shoe from shoe list using product code.
    If shoe exists, return shoe object.
    '''
    
    #get code of shoe from user
    code = input("\nPlease enter the code of the shoes you are looking for: ")
    
    #check if product code exists
    match = None
    for shoe in shoe_list:
        if shoe.code == code:
            match = shoe
            return shoe
    #print if product does not exist
    if match == None:
        print("\nProduct not listed.")
        return ""
        
    
def value_per_item(shoe_list):
    '''Calculate the total value for each shoe object.
    Print the value for all the shoes.
    '''
    
    #empty list to add values in order to tabulate
    shoe_values = []
    #calculate values of each shoe
    for shoe in shoe_list:
        value = (shoe.get_cost())*(shoe.get_quantity())
        shoe_values.append([shoe.product,value])
    #print table of values    
    print(tabulate(shoe_values, headers = ['Product Name:','Total Value:']))
    
    
def highest_qty(shoe_list):
    '''Determine shoe object with highest quantity.
    Print item as being for sale.
    '''
    
    #find shoe with max quantity
    highest_stock = max(shoe_list, key=attrgetter('quantity'))
    #print it as for sale
    print(f"""
    Largest stock: \t {highest_stock.product}
    Quantity: \t {highest_stock.quantity}
    This item is for sale!""")
    

#==========Main Menu=============

#create shoes list
try:
    read_shoes_data(data,shoe_list)
except FileNotFoundError:
    print("File not found.")

#menu
while True:
    menu = str(input("""
    Please select one of the following options:
    -------
    1. Capture new shoe data
    2. View all shoe data
    3. Restock lowest quantity shoe
    4. Search for a shoe
    5. View all shoe values
    6. View highest quantity shoe
    7. Exit program
    : 
    """))
    
    #capture new shoe data
    if menu == '1':
        capture_shoes(shoe_list)
    
    #view all shoe data
    elif menu == '2':
        view_all(shoe_list)
    
    #restock lowest quantity shoe
    elif menu == '3':
        re_stock(shoe_list,data)
    
    #search for a shoe
    elif menu == '4':
        print(str(search_shoe(shoe_list)))
    
    #view all shoe values
    elif menu == '5':
        value_per_item(shoe_list)
    
    #view highest quantity shoe
    elif menu == '6':
        highest_qty(shoe_list)
    
    #exit program
    elif menu == '7':
        exit()
    
    #invalid input
    else:
        print("\nInvalid input. Please try again.")

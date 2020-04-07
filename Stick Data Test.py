from functools import partial
from yahoo_fin.stock_info import *
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#define some global variables
global totReturns   #variable to hold total returns of your current investment
totReturns = 0.0

global displayItems      #variable to hold a list of all displayed items. Use this to
displayItems = list()    #itterate through list and delete/update values

global stockWatchlist     #variable to hold list of stocks to watch along with their info.
stockWatchlist = list()   #displayItems will use these values to update and display to user.

def create_labels():    #get share price and div/yield. Add stock items to stockWatchlist.
    stockticker = stockTickerAdd.get().upper()
    stockprice = "{:.2f}".format(get_live_price(stockticker))
    stockdiv = get_quote_table(stockticker)
    try:
        stockdiv = stockdiv['Forward Dividend & Yield'].split('(')[1].split('%')[0]
    except:
        stockdiv = 'N/A'
    if (stockdiv == 'N/A)'):
        stockdiv = 'N/A'
    #add stock info and placeholders to stockWatchlist
    stockWatchlist.append([stockticker, stockprice, stockdiv, 0, 0, 0, 0, 0, 0, 0, '', 0])

    refresh()   #delete all displayed elements and recreate them.
    stockTickerAdd.delete(0, 'end')

def delete_All():   #delete everything and start over
    for row in displayItems:
        #print(row)
        row.destroy()
    displayItems.clear()
    stockWatchlist.clear()

def remove(record): #remove an entire row (record) from the stockWatchlist
    stockWatchlist.pop(record)
    refresh()   #delete all displayed elements and recreate them from stockWatchlist
    update_items()


def update_items(): #re-calculate all items in stockWatchlist
    totReturns = 0.0
    global TotalReturns
    TotalReturns.destroy()
    i=4
    for items in stockWatchlist:
        items[3] = displayItems[i].get()    #get nr. of shares
        items[4] = displayItems[i+1].get()  #get avg pruchase price per share
        items[5] = '{:.2f}'.format(float(items[3]) * float(items[4]))   #investment amount
        items[6] = '{:.2f}'.format(float(items[1]) * float(items[3]))   #current value of shares
        items[7] = '{:.2f}'.format(float(items[6]) - float(items[5]))   #gain/loss
        items[8] = '{:.2f}'.format(float(items[1]) * get_div(items[2])/100 * float(items[3])/12 *
                                   float(monthsOfDiv.get()))    #div/yield per x months
        items[9] = '{:.2f}'.format(float(items[7]) + float(items[8]))   #investment return (share value + div)
        items[10] = displayItems[i+7].get() #get projected share price
        if(items[10] == ''):
            items[11] = 0
        else:
            items[11] = '{:.2f}'.format((float(items[10]) * float(items[3])) - float(items[5])) #projected returns
        totReturns+= float(items[9])
        i+=len(stockWatchlist[0])+1 #increment to the next row in the displayItems
    totReturns = float('{:.2f}'.format(totReturns)) #format the returns to 2 decimal places
    TotalReturns = tk.Label(scrollable_frame, text=totReturns, bg='gray28', fg='white') #create display item for
    TotalReturns.grid(row=1, column=11, pady=(5,0), padx=(0,0), sticky='nw')            #total returns
    #TotalReturns.place(x=1105, y=140)
    if(totReturns > 0):
        TotalReturns.configure(fg='green3')
    elif(totReturns < 0):
        TotalReturns.configure(fg='red')
    else:
        TotalReturns.configure(fg='white')
    refresh()
    print(stockWatchlist)

def get_div(dividends): #format the dividend to 0 if it's N/A
    if(dividends == 'N/A'):
        return 0
    return float(dividends)



root = tk.Tk()
root.title("Stock Position & Projections")  #window title

frame_main = tk.Frame(root,bg='gray28')     #high-level frame that holds all other frames and canvases
frame_main.grid(row = 0, column = 0)
#frame_main.pack(fill='both', expand=True)
frame_main.grid_rowconfigure(1, weight=1)   #make sure no border is visible
frame_main.grid_columnconfigure(1, weight=1)

container = tk.Frame(frame_main, bg='gray28')    #second-level frame that holds scrollable canvas with
container.grid_rowconfigure(1, weight=1)        #third-level frame which holds all stock data to display
container.grid_rowconfigure(1, weight=1)

canvas=tk.Canvas(container, bg='gray28', highlightthickness=0, width=1000, height=600)
canvas.grid_rowconfigure(1, weight=1)
canvas.grid_columnconfigure(1, weight=1)

scrollable_frame=tk.Frame(canvas, bg='gray28')  #frame that will hold all stock info to display
scrollable_frame.grid_rowconfigure(1, weight=1)
scrollable_frame.grid_columnconfigure(1, weight=1)

scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
scrollable_frame.bind(
    '<Configure>', lambda e:canvas.configure(scrollregion=canvas.bbox('all'))
)

canvas.create_window((0,0), window=scrollable_frame, anchor='nw')
canvas.configure(xscrollcommand=scrollbar.set)

#display title for stock info window
label1 = tk.Label(frame_main, text='Live Stock Data', bg='gray28', fg='navajowhite2')
label1.config(font=('Times New Roman', 30, 'bold'))
label1.grid(row=0, column=0, columnspan=6, pady=(5,0))

#stock ticker label
stockTickerLbl = tk.Label(frame_main, text='Stock Ticker:', bg='gray28', fg='white')
stockTickerLbl.grid(row=1, column=0,pady=(20,0), padx=(0,2), sticky='ne')

#stock ticker input field
stockTickerAdd = tk.Entry(frame_main, bg='gray35', fg='white', highlightthickness=0, width=6)
stockTickerAdd.grid(row=1, column=1, pady=(20,0), padx=(0,0), sticky='nw')


#create the Add button to add stock ticker to stockWatchlist
Add = tk.Button(frame_main, text='Add', command = create_labels, bg='gray28', highlightthickness=0,
                highlightbackground = 'gray35')
Add.grid(row=1, column=2, pady=(20,0), padx=(0,20), sticky='nw')

#create the Clear All button to clear the stockWatchlist and displayed items
ClearAll = tk.Button(frame_main, text='Clear All', command = delete_All, bg='gray28', highlightthickness=0,
                     highlightbackground = 'gray35')
ClearAll.grid(row=1, column=3, pady=(20,0), padx=(0,20),sticky='nw')

#create the Update button to updated all displayed data after input fields have been changed by user
Update = tk.Button(frame_main, text='Update', command = update_items, bg='gray28', highlightthickness=0,
                   highlightbackground = 'gray35')
Update.grid(row=1, column=5, columnspan=2, pady=(20,0), padx=(0,640), sticky='nw')


#display all the column headers
#stock column
stockHeader = tk.Label(scrollable_frame, text='Stock', font=('Arial', 14, 'bold'), bg='gray28', fg='skyblue3')
stockHeader.grid(row=0, column=0, columnspan=2, pady=(20,0), padx=(30,25), sticky='nw')

#price column
priceHeader = tk.Label(scrollable_frame, text='Price', font=('Arial', 14, 'bold'), bg='gray28', fg='skyblue3')
priceHeader.grid(row=0, column=2, pady=(20,0), padx=(0,25), sticky='nw')

#div/yield column, etc...
divHeader = tk.Label(scrollable_frame, text='Div / Yield', font=('Arial', 14, 'bold'), bg='gray28', fg='skyblue3')
divHeader.grid(row=0, column=3, pady=(20,0), padx=(0,25), sticky='nw')

sharesHeader = tk.Label(scrollable_frame, text='Shares', font=('Arial', 14, 'bold'), bg='gray28', fg='skyblue3')
sharesHeader.grid(row=0, column=4, pady=(20,0), padx=(0,25), sticky='nw')

sharePriceHeader = tk.Label(scrollable_frame, text='Avg Price\nPaid', font=('Arial', 14, 'bold'), bg='gray28',
                            fg='skyblue3')
sharePriceHeader.grid(row=0, column=5, pady=(20,0), padx=(0,25), sticky='nw')

invAmntHeader = tk.Label(scrollable_frame, text='Invested\nAmount', font=('Arial', 14, 'bold'), bg='gray28',
                         fg='skyblue3')
invAmntHeader.grid(row=0, column=6, pady=(20,0), padx=(0,25), sticky='nw')

curPosHeader = tk.Label(scrollable_frame, text='Current\nPosition', font=('Arial', 14, 'bold'), bg='gray28',
                        fg='skyblue3')
curPosHeader.grid(row=0, column=7, pady=(20,0), padx=(0,25), sticky='nw')

gainLossHeader = tk.Label(scrollable_frame, text='Gain / Loss', font=('Arial', 14, 'bold'), bg='gray28', fg='skyblue3')
gainLossHeader.grid(row=0, column=8, pady=(20,0), padx=(0,25), sticky='nw')

div3moHeader = tk.Label(scrollable_frame, text='Div / Months', font=('Arial', 14, 'bold'), bg='gray28', fg='skyblue3')
div3moHeader.grid(row=0, column=9, pady=(20,0), padx=(0,25), sticky='nw')

#input field for how many months of dividends have passed
monthsOfDiv = tk.Entry(scrollable_frame, bg='gray35', fg='white', width=4, highlightthickness=0)
monthsOfDiv.insert(0, '3')
monthsOfDiv.grid(row=1, column=9, pady=(0,0), padx=(0,25), sticky='n')

invReturnHeader = tk.Label(scrollable_frame, text='Investment\nReturn', font=('Arial', 14, 'bold'), bg='gray28',
                           fg='skyblue3')
invReturnHeader.grid(row=0, column=10, pady=(20,0), padx=(0,25), sticky='nw')

totReturnHeader = tk.Label(scrollable_frame, text='Total\nReturns', font=('Arial', 14, 'bold'), bg='gray28',
                           fg='skyblue3')
totReturnHeader.grid(row=0, column=11, pady=(20,0), padx=(0,25), sticky='nw')

TotalReturns = tk.Label(scrollable_frame, text='', bg='gray28', fg='white')
TotalReturns.grid(row=1, column=11, pady=(20,0), padx=(0,25), sticky='nw')

projSharePrice = tk.Label(scrollable_frame, text='Projected\nShare Price', font=('Arial', 14, 'bold'), bg='gray28',
                          fg='skyblue3')
projSharePrice.grid(row=0, column=12, pady=(20,0), padx=(0,25), sticky='nw')

projReturn = tk.Label(scrollable_frame, text='Projected\nReturn', font=('Arial', 14, 'bold'), bg='gray28',
                      fg='skyblue3')
projReturn.grid(row=0, column=13, pady=(20,0), padx=(0,25), sticky='nw')




def refresh():  #delete all displayed items and recreate them from the stockWatchlist
    for row in displayItems:
        #print(row)
        row.destroy()
    displayItems.clear()
    i = 0
    for row in stockWatchlist:    #for each row in the stockWatchlist, create a grid item and distplay it
        #remove button
        displayItems.append(tk.Button(scrollable_frame, height = 1, text='-', command=partial(remove, i), bg='gray28',
                                     highlightthickness=0, highlightbackground='gray35'))
        displayItems[-1].grid(row=i+1, column=0,pady=(32,0), padx=(5,2),sticky='nw')

        #stock ticker
        displayItems.append(tk.Label(scrollable_frame, text=row[0], bg='gray28', fg='white'))
        displayItems[-1].grid(row=i+1, column=1,pady=(30,0), padx=(10,2),sticky='nw')

        #stock price
        displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[1]))), bg='gray28', fg='white'))
        displayItems[-1].grid(row=i+1, column=2,pady=(30,0), padx=(0,2),sticky='nw')

        #divident yield
        displayItems.append(tk.Label(scrollable_frame, text=row[2], bg='gray28', fg='white'))
        displayItems[-1].grid(row=i+1, column=3,pady=(30,0), padx=(0,2),sticky='nw')

        #shares purchased
        displayItems.append(tk.Entry(scrollable_frame, bg='gray35', fg='white', highlightthickness=0, width=4))
        displayItems[-1].insert(0, row[3])
        displayItems[-1].grid(row=i+1, column=4,pady=(30,0), padx=(0,2),sticky='nw')

        #price per share
        displayItems.append(tk.Entry(scrollable_frame, bg='gray35', fg='white', highlightthickness=0, width=6))
        displayItems[-1].insert(0, row[4])
        displayItems[-1].grid(row=i+1, column=5,pady=(30,0), padx=(0,2),sticky='nw')

        #invested amount
        displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[5]))), bg='gray28', fg='white'))
        displayItems[-1].grid(row=i+1, column=6,pady=(30,0), padx=(0,2), sticky='nw')

        #current position
        displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[6]))), bg='gray28', fg='white'))
        displayItems[-1].grid(row=i+1, column=7,pady=(30,0), padx=(0,2),sticky='nw')

        #gain/loss of current stock shares. if gain > 0, display in green, if < 0 display in red, if 0 display in white
        if(float(row[7]) > 0):
            displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[7]))), bg='gray28',
                                         fg='green3'))
            displayItems[-1].grid(row=i+1, column=8,pady=(30,0), padx=(0,2),sticky='nw')
        elif(float(row[7]) < 0):
            displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[7]))), bg='gray28',
                                         fg='red'))
            displayItems[-1].grid(row=i+1, column=8,pady=(30,0), padx=(0,2),sticky='nw')
        else:
            displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[7]))), bg='gray28',
                                         fg='white'))
            displayItems[-1].grid(row=i+1, column=8,pady=(30,0), padx=(0,2),sticky='nw')

        #dividends after x months
        displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[8]))), bg='gray28', fg='white'))
        displayItems[-1].grid(row=i+1, column=9,pady=(30,0), padx=(0,2), sticky='nw')

        #investment return (including dividends). green if > 0, red if < 0, white if = 0
        if(float(row[9]) > 0):
            displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[9]))), bg='gray28',
                                         fg='green3'))
            displayItems[-1].grid(row=i+1, column=10,pady=(30,0), padx=(0,2),sticky='nw')
        elif(float(row[9]) < 0):
            displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[9]))), bg='gray28',
                                         fg='red'))
            displayItems[-1].grid(row=i+1, column=10,pady=(30,0), padx=(0,2),sticky='nw')
        else:
            displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[9]))), bg='gray28',
                                         fg='white'))
            displayItems[-1].grid(row=i+1, column=10,pady=(30,0), padx=(0,2),sticky='nw')

        #projected share price - price you think the stock will reach
        displayItems.append(tk.Entry(scrollable_frame, bg='gray35', fg='white', highlightthickness=0, width=6))
        displayItems[-1].insert(0, row[10])
        displayItems[-1].grid(row=i+1, column=12,pady=(30,0), padx=(4,60), sticky='nw')

        #projected returns based on user specified future stock price
        if(float(row[11]) > 0):
            displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[11]))), bg='gray28',
                                         fg='green3'))
            displayItems[-1].grid(row=i+1, column=13,pady=(30,0), padx=(0,25), sticky='nw')

        elif(float(row[11]) < 0):
            displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[11]))), bg='gray28',
                                         fg='red'))
            displayItems[-1].grid(row=i+1, column=13,pady=(30,0), padx=(0,25),sticky='nw')
        else:
            displayItems.append(tk.Label(scrollable_frame, text=('{:,.2f}'.format(float(row[11]))), bg='gray28',
                                         fg='white'))
            displayItems[-1].grid(row=i+1, column=13,pady=(30,0), padx=(2,60), sticky='nw')

        i += 1

#place the container frame, canvas, and scrollbar in the window
container.grid(row=2, column=0, columnspan=6)
canvas.pack(fill="both", expand=True)
scrollbar.pack(side="bottom", fill="x")

root.mainloop()
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import re
from value_list import *
from create_table_commands import *
from airports import airport_info
from PIL import Image, ImageTk

# --------------------------------SQlite3------------------------------------#
# Connect to database
conn = sqlite3.connect('airline.db')
## create cursor
c = conn.cursor()

########################## RUN ONLY ON FORKED COPY ######################
################# Otherwise please comment out !!!!! ####################
#########################################################################
# ## create tables
# [c.execute(command) for command in create_table_commands]
#########################################################################
#########################################################################

c.execute('''PRAGMA foreign_keys = ON;''')

# --------------------------------Initialise----------------------------------#
# initialise app
master = Tk()
master.title("Flight Database")
master.minsize(width=600, height=500)

pk_bg = "aquamarine1"
junc_bg = "bisque1"
main_button_color = "burlywood1"


# ---------------------------"Select Table" Header ---------------------------#
# Show ER Diagram
def ER_diagram():
  # create new window and set at top level
  schema_window = Toplevel(master)
  schema_window.title("E-R Diagram")
  schema_window.minsize(width=1050, height=650)
  schema_window.attributes('-topmost', 1)

  # Create image file and add show on new window.

  # Make sure to replace "ER_diagram.png" with the correct path to your image file
  image = Image.open("ER_diagram.png")
  resize_image = image.resize((1000, 600))
  resize_image.save("ER_diagram_resized.png")
  ER_diagram = ImageTk.PhotoImage(file="ER_diagram_resized.png")

  ER_diagram_widget = Label(schema_window, image=ER_diagram)
  ER_diagram_widget.image = ER_diagram
  ER_diagram_widget.place(x=10, y=10)

  return


def flight_stats():

  stats_window = Toplevel(master)

  stats_window.minsize(width=600, height=500)
  stats_window.title(f"Custom Flight Summary")

  # pull value from pilots table to get pilot listbox values
  c.execute("SELECT DISTINCT PilotID FROM pilots")
  pilot_list = [pilot[0] for pilot in c.fetchall()]
  # pull value from flights table (aircraftID column) to get Aircraft listbox values
  c.execute("SELECT DISTINCT AircraftID FROM Aircrafts")
  aircraft_list = [aircraft[0] for aircraft in c.fetchall()]
  # pull values from flight table (DepartureAirport, ArrivalAirport columns) to populate from_value list
  c.execute("SELECT DISTINCT DepartureAirport FROM Flights")
  departure_apt_list = [airport[0] for airport in c.fetchall()]
  c.execute("SELECT DISTINCT ArrivalAirport FROM Flights")
  arrival_apt_list = [airport[0] for airport in c.fetchall()]

  # pull values from Destination table (City Column where Destination ID is in DepartureAirport and ArrivalAirport in Flight table)
  c.execute(
      "SELECT DISTINCT City FROM Destinations where DestinationID in (SELECT DepartureAirport FROM Flights)"
  )
  departure_city_list = [city[0] for city in c.fetchall()]
  c.execute(
      "SELECT DISTINCT City FROM Destinations where DestinationID in (SELECT ArrivalAirport FROM Flights)"
  )
  arrival_city_list = [city[0] for city in c.fetchall()]

  # pull values from Destination table (Country Column where Destination ID is in DepartureAirport and ArrivalAirport in Flight table)
  c.execute(
      "SELECT DISTINCT Country FROM Destinations where DestinationID in (SELECT DepartureAirport FROM Flights)"
  )
  departure_country_list = [country[0] for country in c.fetchall()]
  c.execute(
      "SELECT DISTINCT Country FROM Destinations where DestinationID in (SELECT ArrivalAirport FROM Flights)"
  )
  arrival_country_list = [country[0] for country in c.fetchall()]

  # Create widgets
  # Label: Search Flights
  search_flights_label = Label(
      stats_window,
      text="Search Flights",
      font=("Arial", 10, 'bold'),
  )

  from_label = Label(stats_window, text="From: ")
  from_category = ttk.Combobox(
      stats_window,
      values=["--Select--", "Country", "City", "Airport"],
      width=10,
      state="readonly")
  from_category.set(value="--Select--")
  from_values = ttk.Combobox(stats_window,
                             values=["--Select--"],
                             width=14,
                             state="readonly")
  to_label = Label(stats_window, text="To: ")
  to_category = ttk.Combobox(
      stats_window,
      values=["--Select--", "Country", "City", "Airport"],
      width=10,
      state="readonly")
  to_category.set(value="--Select--")
  to_values = ttk.Combobox(stats_window,
                           values=["--Select--"],
                           width=14,
                           state="readonly")

  date_label = Label(stats_window, text="In Period: ")

  from_date_label = Label(stats_window, text="From: ")
  from_date_entry = Entry(stats_window, width=12)
  to_date_label = Label(stats_window, text="To: ")
  to_date_entry = Entry(stats_window, width=12)
  date_example_label_1 = Label(stats_window,
                               text="YYYY-MM-DD",
                               font=("Arial", 8, 'italic'),
                               fg="dimgray")
  date_example_label_2 = Label(stats_window,
                               text="YYYY-MM-DD",
                               font=("Arial", 8, 'italic'),
                               fg="dimgray")

  # departure & arrival time
  depart_label = Label(stats_window, text="Departs: ")
  depart_category = ttk.Combobox(stats_window,
                                 values=["--Select--", "By", "After"],
                                 width=10,
                                 state="readonly")
  depart_category.set(value="--Select--")
  depart_entry = Entry(stats_window, width=14, state="readonly")
  arrive_label = Label(stats_window, text="Arrives: ")
  arrive_category = ttk.Combobox(stats_window,
                                 values=["--Select--", "By", "After"],
                                 width=10,
                                 state="readonly")
  arrive_category.set(value="--Select--")
  arrive_entry = Entry(stats_window, width=14, state="readonly")
  time_example_label_1 = Label(stats_window,
                               text="HH:MM",
                               font=("Arial", 8, 'italic'),
                               fg="dimgray")
  time_example_label_2 = Label(stats_window,
                               text="HH:MM",
                               font=("Arial", 8, 'italic'),
                               fg="dimgray")

  # Label: Assigned to Pilot(s):
  pilots_label = Label(stats_window, text="Assigned to Pilot(s): ")

  pilots_instruction = Label(stats_window,
                             text="Select all pilot IDs",
                             font=("Arial", 8, "italic"),
                             fg='dimgray')
  pilots_listbox = Listbox(stats_window,
                           height=12,
                           width=14,
                           exportselection=False,
                           selectmode="multiple")
  pilots_scrollbar = ttk.Scrollbar(stats_window, orient='vertical')

  pilots_listbox.config(yscrollcommand=pilots_scrollbar.set)
  for pilot in pilot_list:
    pilots_listbox.insert(pilot_list.index(pilot), pilot)

  # Label: Aircraft Model
  aircraft_label = Label(stats_window, text="Assigned to Aircraft(s): ")
  aircraft_instruction = Label(stats_window,
                               text="Select all aircraft IDs",
                               font=("Arial", 8, "italic"),
                               fg='dimgray')

  # Dropdown: Aircraft Model
  aircraft_listbox = Listbox(stats_window,
                             height=12,
                             width=14,
                             exportselection=False,
                             selectmode="multiple")
  aircrafts_scrollbar = ttk.Scrollbar(stats_window, orient='vertical')

  aircraft_listbox.config(yscrollcommand=aircrafts_scrollbar.set)
  for aircraft in aircraft_list:
    aircraft_listbox.insert(aircraft_list.index(aircraft), aircraft)

  # Label: Order by
  order_by_label = Label(stats_window, text="Order by: ")
  order_by_ascdec = ttk.Combobox(
      stats_window,
      values=["--Select--", "Ascending", "Descending"],
      width=10,
      state="readonly")
  order_by_ascdec.set(value="--Select--")
  order_by_field = ttk.Combobox(stats_window,
                                values=["--Select--"],
                                width=14,
                                state="readonly")

  # place widgets
  row1_y = 20
  row2_y = row1_y + 30
  row3_y = row2_y + 30
  row4_y = row3_y + 30
  row5_y = row4_y + 120
  row6_y = row5_y + 30

  # Row 1
  search_flights_label.grid(row=0, column=0, sticky=E, padx=10, pady=10)

  # Row 2
  from_label.grid(row=1, column=0, sticky=E, padx=5, pady=2)
  from_category.grid(row=1, column=1, sticky=W, padx=5, pady=2)
  from_values.grid(row=1, column=2, sticky=W, padx=5, pady=2)
  to_label.grid(row=1, column=3, sticky=E, padx=10, pady=2)
  to_category.grid(row=1, column=4, sticky=W, padx=5, pady=2)
  to_values.grid(row=1, column=5, sticky=W, padx=5, pady=2)

  # Row 3, 4
  date_label.grid(row=3, column=0, sticky=SE, padx=5, pady=6)
  from_date_label.grid(row=4, column=0, sticky=E, padx=5)
  from_date_entry.grid(row=4, column=1, sticky=W, padx=5)
  to_date_label.grid(row=4, column=2, sticky=W, padx=5)
  to_date_entry.grid(row=4, column=2, sticky=E, padx=5)
  date_example_label_1.grid(row=5, column=1, sticky=W, padx=9)
  date_example_label_2.grid(row=5, column=2, sticky=E, padx=30)

  # Row 5
  pilots_label.grid(row=6, column=0, sticky=NE, padx=5, pady=10)

  pilots_instruction.grid(row=6,
                          column=1,
                          columnspan=2,
                          sticky=NW,
                          padx=5,
                          pady=12)
  pilots_listbox.grid(row=6, column=1, columnspan=2, sticky=W, padx=5, pady=30)
  pilots_scrollbar.grid(row=6,
                        column=1,
                        columnspan=2,
                        sticky=NS,
                        padx=120,
                        pady=30)
  pilots_scrollbar.config(command=pilots_listbox.yview)
  pilots_listbox.config(yscrollcommand=pilots_scrollbar.set)

  aircraft_label.grid(row=6, column=3, sticky=NE, padx=5, pady=10)

  aircraft_instruction.grid(row=6,
                            column=4,
                            columnspan=2,
                            sticky=NW,
                            padx=5,
                            pady=12)
  aircraft_listbox.grid(row=6,
                        column=4,
                        columnspan=2,
                        sticky=SW,
                        padx=5,
                        pady=30)

  aircrafts_scrollbar.grid(row=6,
                           column=4,
                           columnspan=2,
                           sticky=NS,
                           padx=80,
                           pady=30)
  aircrafts_scrollbar.config(command=aircraft_listbox.yview)
  aircraft_listbox.config(yscrollcommand=aircrafts_scrollbar.set)
  # Row 7 & 8
  depart_label.grid(row=7, column=0, sticky=SE, padx=5, pady=0)
  depart_category.grid(row=7, column=1, sticky=SW, padx=5, pady=0)
  depart_entry.grid(row=7, column=2, sticky=SW, padx=5, pady=0)
  arrive_label.grid(row=7, column=3, sticky=SE, padx=5, pady=0)
  arrive_category.grid(row=7, column=4, sticky=SW, padx=5, pady=0)
  arrive_entry.grid(row=7, column=5, sticky=SW, padx=5, pady=0)
  time_example_label_1.grid(row=8, column=2, sticky=NW, padx=9)
  time_example_label_2.grid(row=8, column=5, sticky=NW, padx=9)
  # Row 9
  order_by_label.grid(row=9, column=0, sticky=NE, padx=5, pady=10)
  order_by_ascdec.grid(row=9, column=1, sticky=NW, padx=5, pady=10)
  order_by_field.grid(row=9,
                      column=2,
                      columnspan=2,
                      sticky=NW,
                      padx=5,
                      pady=10)

  # FUNCTION TO SEARCH FLIGHTS
  def set_from_values(event):
    if from_category.get() == "--Select--":
      from_values['vallues'] = []
    if from_category.get() == "Airport":
      from_values['values'] = departure_apt_list
    if from_category.get() == "City":
      from_values['values'] = departure_city_list
    if from_category.get() == "Country":
      from_values['values'] = departure_country_list
    return

  def set_to_values(event):
    if to_category.get() == "--Select--":
      to_values['values'] = []
    if to_category.get() == "Airport":
      to_values['values'] = arrival_apt_list
    if to_category.get() == "City":
      to_values['values'] = arrival_city_list
    if to_category.get() == "Country":
      to_values['values'] = arrival_country_list
    return

  def set_order_by_values(event):
    if order_by_ascdec.get() == "--Select--":
      order_by_field['values'] = []
    if order_by_ascdec.get() == "Ascending" or order_by_ascdec.get(
    ) == "Descending":
      order_by_field['values'] = [
          "FlightID", "FlightDuration", "DepartureDateTime", "ArrivalDateTime",
          "AircraftID"
      ]
    return

  def unlock_from_time(event):
    if depart_category.get() == "--Select--":
      depart_entry.configure(state="readonly")
    else:
      depart_entry.configure(state="normal")
    return

  def unlock_to_time(event):
    if arrive_category.get() == "--Select--":
      arrive_entry.configure(state="readonly")
    else:
      arrive_entry.configure(state="normal")
    return

  def search_flights():

    # Declare empty statements  (value to be set later)
    from_to_statement = ""
    date_period_statement = ""
    pilot_statement = ""
    aircraft_statement = ""
    time_constraint_statement = ""
    order_statement = ""

    # GET ALL VALUES IN ENTRIES and form statements
    from_area = from_category.get(
    ) if from_category.get() != "--Select--" else ""
    from_location = from_values.get(
    ) if from_category.get() != "--Select--" else ""
    if from_area != "" and from_location == "":
      from_area = ""

    to_area = to_category.get() if to_category.get() != "--Select--" else ""
    to_location = to_values.get() if to_category.get() != "--Select--" else ""
    if to_area != "" and to_location == "":
      to_area = ""

    from_statement = ""
    if from_area == "":
      from_statement = ""
    if from_area == "Airport":
      from_statement = f"DepartureAirport = '{from_location}'"
    if from_area == "City":
      from_statement = f"DepartureAirport in (SELECT DestinationID FROM destinations WHERE City = '{from_location}')"

    to_statement = ""
    if to_area == "":
      to_statement = ""
    if to_area == "Airport":
      to_statement = f"ArrivalAirport = '{from_location}'"
    if to_area == "City":
      to_statement = f"ArrivalAirport in (SELECT DestinationID FROM destinations WHERE City = '{to_location}')"

    if from_statement == "":
      if to_statement == "":
        from_to_statement = ""
      else:
        from_to_statement = to_statement
    else:
      if to_statement == '':
        from_to_statement = from_statement
      else:
        from_to_statement = f"{from_statement} and {to_statement}"

    # Date period statement
    from_date = from_date_entry.get()
    to_date = to_date_entry.get()

    from_date_statement = ""
    if from_date == "":
      from_date_statement = ""
    if from_date != "":
      from_date_statement = f"DepartureDate >= date('{from_date}')"

    to_date_statement = ""
    if to_date == "":
      to_date_statement = ""
    if to_date != "":
      to_date_statement = f"DepartureDate <= date('{to_date}')"

    if from_date_statement == "":
      if to_date_statement == "":
        date_period_statement = ""
      else:
        date_period_statement = to_date_statement
    else:
      if to_date_statement == '':
        date_period_statement = from_date_statement
      else:
        date_period_statement = f"{from_date_statement} and {to_date_statement}"

    # Pilot statement
    selected_pilots = [
        "'" + pilots_listbox.get(index) + "'"
        for index in pilots_listbox.curselection()
    ] if len(pilots_listbox.curselection()) > 0 else ""
    if len(selected_pilots) > 0:
      selected_pilot_string = ', '.join(selected_pilots)
      pilot_statement = f"FLIGHTID in (SELECT FLIGHTID FROM PILOT_FLIGHT_JUNC WHERE PilotID in ({selected_pilot_string}))"
    else:
      pilot_statement = ""

    # Aircraft statement
    selected_aircraft = [
        "'" + aircraft_listbox.get(index) + "'"
        for index in aircraft_listbox.curselection()
    ] if len(aircraft_listbox.curselection()) > 0 else ""
    if len(selected_aircraft) > 0:
      selected_aircraft_string = ', '.join(selected_aircraft)
      aircraft_statement = f"AircraftID in ({selected_aircraft_string})"
    else:
      aircraft_statement = ""

    # arrive/depart before/after TIME input
    depart_before_after = depart_category.get(
    ) if depart_category.get() != "--Select--" else ""
    depart_time = depart_entry.get(
    ) + ":00" if depart_before_after != "" else ""
    if depart_time == ":00" and depart_before_after != "":
      depart_time = ""
      depart_before_after = ""

    depart_time_constraint_statement = ""
    if depart_before_after == "":
      depart_time_constraint_statement = ""
    if depart_before_after == "By":
      depart_time_constraint_statement = f"DepartureTime <= time('{depart_time}')"
    if depart_before_after == "After":
      depart_time_constraint_statement = f"DepartureTime >= time('{depart_time}')"

    arrive_before_after = arrive_category.get(
    ) if arrive_category.get() != "--Select--" else ""
    arrive_time = arrive_entry.get(
    ) + ":00" if arrive_before_after != "" else ""
    if arrive_time == ":00" and arrive_before_after != "":
      arrive_time = ""
      arrive_before_after = ""

    arrive_time_constraint_statement = ""
    if arrive_before_after == "":
      arrive_time_constraint_statement = ""
    if arrive_before_after == "By":
      arrive_time_constraint_statement = f"ArrivalTime <= time('{arrive_time}')"
    if arrive_before_after == "After":
      arrive_time_constraint_statement = f"ArrivalTime >= time('{arrive_time}')"

    if depart_time_constraint_statement == "":
      if arrive_time_constraint_statement == "":
        time_constraint_statement = ""
      else:
        time_constraint_statement = arrive_time_constraint_statement
    else:
      if arrive_time_constraint_statement == "":
        time_constraint_statement = depart_time_constraint_statement
      else:
        time_constraint_statement = f"{depart_time_constraint_statement} and {arrive_time_constraint_statement}"

    # ORDER BY
    order_type = order_by_ascdec.get(
    ) if order_by_ascdec.get() != "--Select--" else ""
    if order_type == "Ascending":
      order_type = "asc"
    if order_type == "Descending":
      order_type = "desc"

    order_field = order_by_field.get() if order_type != "--Select--" else ""

    if order_type != "" and order_field == "":
      order_type = ""

    # if order by departure/arrival DateTime
    if order_field == "DepartureDateTime":
      order_statement = f"order by DepartureDate {order_type}, DepartureTime {order_type}"
    if order_field == "ArrivalDateTime":
      order_statement = f"order by ArrivalDate {order_type}, ArrivalTime {order_type}"

    # if order by other fields
    if order_field not in ["DepartureDateTime", "ArrivalDateTime"]:
      order_statement = "" if order_type == "" else f"order by {order_field} {order_type}"

    where_condition_list = [
        from_to_statement, date_period_statement, pilot_statement,
        aircraft_statement, time_constraint_statement
    ]
    where_condition_list = [x for x in where_condition_list if x != ""]
    where_condition_string = " where "
    if len(where_condition_list) == 0:
      where_condition_string = ""
    else:
      for i in range(len(where_condition_list)):
        if i < len(where_condition_list) - 1:

          where_condition_string += where_condition_list[i] + " and "
        else:
          where_condition_string += where_condition_list[i]

    flight_search_query = f"select * from Flights {where_condition_string} {order_statement}"

    # Execute the query
    # get number of flights
    c.execute(f"select count(*) from ({flight_search_query})")
    flight_count = c.fetchone()[0]

    # create new window for display flight summary
    flight_summary_window = Toplevel(stats_window)
    flight_summary_window.title("Flights Found")

    # show the number of flights found as label
    flight_count_label = Label(flight_summary_window,
                               text=f"Summary: {flight_count} flights found",
                               font=(font, 9, 'bold'),
                               fg='blue')
    flight_count_label.pack(side=TOP, anchor=NW)

    # get flight records
    c.execute(flight_search_query)
    flight_records = c.fetchall()

    # get list of flightIDs
    flight_ids = [x[0] for x in flight_records]
    column_names = [description[0]
                    for description in c.description] + ["AssociatedPilots"]
    columns = tuple(column_names)

    # get the list of pilots associated with this flight

    pilotID_column_values = []
    for flight_id in flight_ids:
      c.execute(
          f"select distinct PilotID from pilot_flight_junc where FlightID = '{flight_id}'"
      )
      pilot_ids = c.fetchall()
      pilot_ids = [x[0] for x in pilot_ids]
      comma_delimited_pilotID = " "
      if len(pilot_ids) > 0:
        comma_delimited_pilotID = ', '.join(pilot_ids)
      pilotID_column_values.append(comma_delimited_pilotID)

    # show flight records
    table_view = ttk.Treeview(flight_summary_window,
                              columns=columns,
                              show="headings")
    for column in columns:
      table_view.column(width=120, column=column)

    for i in range(len(columns)):
      table_view.heading(columns[i], text=columns[i])
    table_view.pack()
    for i in range(len(flight_records)):
      to_list = list(flight_records[i])
      to_list.append(pilotID_column_values[i])

      obs = to_list
      table_view.insert('', 'end', values=obs)

    return

  depart_category.bind("<<ComboboxSelected>>", unlock_from_time)
  arrive_category.bind("<<ComboboxSelected>>", unlock_to_time)
  from_category.bind("<<ComboboxSelected>>", set_from_values)
  to_category.bind("<<ComboboxSelected>>", set_to_values)
  order_by_ascdec.bind("<<ComboboxSelected>>", set_order_by_values)
  search_button = Button(stats_window,
                         text="Search",
                         font=("Arial", 10, 'bold'),
                         command=search_flights,
                         bg=pk_bg,
                         width=8)
  search_button.grid(row=0, column=1, sticky=W, padx=5, pady=10)
  return


def view_junction_table():
  junction_viewer_window = Toplevel(master)
  junction_viewer_window.attributes('-topmost', 1)
  junction_viewer_window.minsize(width=600, height=500)
  junction_viewer_window.title(f"Junction Table Records: Pilot and Flights")

  c.execute(f"SELECT distinct * FROM pilot_flight_junc order by pilotID")
  records = c.fetchall()
  columns = tuple([description[0] for description in c.description])
  table_view = ttk.Treeview(junction_viewer_window,
                            columns=columns,
                            show="headings")
  for column in columns:
    table_view.column(width=120, column=column)

  for i in range(len(columns)):
    table_view.heading(columns[i], text=columns[i])
  table_view.pack()
  for obs in records:
    table_view.insert('', 'end', values=obs)
  # get the count of rows retrieved and show in view title
  c.execute('''SELECT count(*) FROM 
                              (SELECT DISTINCT * FROM pilot_flight_junc)''')

  row_count = c.fetchone()[0]

  junction_viewer_window.title(
      f"Junction Table Records: {row_count} Pilot and Flights Associations)")
  return


# Table select dropdown
def menu_heading(master, table_name):
  window = Toplevel(master)
  window.minsize(width=1000, height=800)
  window.title(f"{table_name} Records")
  #window.attributes('-fullscreen', True)
  # select table prompt
  table_label = Label(window, text="Select Table:", font=(font, 9, 'bold'))
  # dropdown list
  table_dropdown = ttk.Combobox(window, state="readonly", values=table_list)

  table_dropdown.set("Please select")
  table_label.place(x=20, y=20)
  table_dropdown.place(x=130, y=20)
  # saved selected table value
  table_selected = table_dropdown.get()
  # ER scheme viewer
  ER_button = Button(window,
                     text="Schema Viewer",
                     command=ER_diagram,
                     height=1,
                     bg='cadetblue2')
  ER_button.place(x=470, y=18)
  junction_button = Button(window,
                           text="Pilot-Flight Junction",
                           command=view_junction_table,
                           height=1,
                           bg='antiquewhite2')
  ER_button.place(x=630, y=18)
  junction_button.place(x=470, y=18)

  return window, table_dropdown


# ---------------------------Menu Specific Functions---------------------------#
# ---------------------------------INSERT----------------------------------#
def insert():

  # assign new window and dropdown list by calling heading generator

  insert_window, table_dropdown = menu_heading(master, "Insert")

  # create empty containers to store field labels and entry boxes
  label_dict = {}
  entry_dict = {}
  constraints_dict = {}
  fields = []

  def table_viewer():
    # table viewer window
    if table_dropdown.get() == "Please select":
      messagebox.showerror("Error",
                           "Please select a table",
                           parent=insert_window)
      return

    table_viewer_window = Toplevel(insert_window)
    table_viewer_window.minsize(width=600, height=500)
    table_viewer_window.title(f"{table_dropdown.get()} Records")

    c.execute(f"SELECT * FROM {table_dropdown.get()}")
    records = c.fetchall()
    columns = tuple([description[0] for description in c.description])
    table_view = ttk.Treeview(table_viewer_window,
                              columns=columns,
                              show="headings")
    for column in columns:
      table_view.column(width=120, column=column)

    for i in range(len(columns)):
      table_view.heading(columns[i], text=columns[i])
    table_view.pack()
    for obs in records:
      table_view.insert('', 'end', values=obs)
    # get the count of rows retrieved and show in view title
    c.execute(f"SELECT count(*) FROM {table_dropdown.get()}")
    row_count = c.fetchone()[0]
    table_viewer_window.title(
        f"{table_dropdown.get()} Search View: {row_count} observations found")
    return

  # declare function to show fields and textboxes

  def show_fields_textbox(event):

    # Get the selected table name and all field names
    table_name = table_dropdown.get()
    c.execute(f"SELECT * FROM {table_name}")
    fields = [description[0] for description in c.description]
    if table_name == "Pilots":
      fields.append("FlightID")
    if table_name == "Flights":
      fields.remove("DepartureDateTime")
      fields.remove("ArrivalDateTime")
      fields.append("PilotID")
    # delete existing labels and entryboxes
    for label in label_dict.values():
      label.destroy()
    for entry in entry_dict.values():
      entry.destroy()
    for constraint in constraints_dict.values():
      constraint.destroy()

    label_dict.clear()
    entry_dict.clear()
    constraints_dict.clear()
    # create new labels and entryboxes
    # set axis
    x = 20
    y = 80

    c.execute("SELECT FlightID FROM Flights")
    flightIDs = c.fetchall()
    flightID_existing = [flight[0] for flight in flightIDs]

    c.execute("SELECT PilotID FROM Pilots")
    pilotIDs = c.fetchall()
    pilotID_existing = [pilot[0] for pilot in pilotIDs]

    for field in fields:
      # create label
      label_dict[field] = Label(insert_window, text=field)

      # create input box and add constraints
      ## -------------------------------------------------------Pilot table
      if table_name == "Pilots":
        ### create dropdown boxes for restricted fields
        # ALL flightIDs
        if field == "PilotID":
          entry_dict[field] = Entry(insert_window, bg=pk_bg)

        elif field == "Gender":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=gender_list)
        elif field == "Nationality":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=nationalities)
        elif field == "Seniority":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=seniorities)
        elif field == "FlightID":
          entry_dict[field] = Listbox(insert_window,
                                      selectmode="multiple",
                                      exportselection=False,
                                      bg=junc_bg)

          for flightID in flightID_existing:
            entry_dict[field].insert(flightID_existing.index(flightID),
                                     flightID)
        else:
          entry_dict[field] = Entry(insert_window)

        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)
        if field == "PilotID":
          constraints_dict[field] = Label(
              insert_window,
              text="Primary key: 6-digit code, e.g. AA03XY",
              font=(font, 8, 'bold'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FirstName":
          constraints_dict[field] = Label(insert_window,
                                          text="e.g. William",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "LastName":
          constraints_dict[field] = Label(insert_window,
                                          text="e.g. Smith",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "MiddleName":
          constraints_dict[field] = Label(insert_window,
                                          text="(Optional)",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DateOfBirth" or field == "DateHired":
          constraints_dict[field] = Label(insert_window,
                                          text="YYYY-MM-DD, e.g. 1999-12-31",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "LicenseNumber":
          constraints_dict[field] = Label(
              insert_window,
              text="11-digit code, e.g. QWER1234UIO",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FlightHours":
          constraints_dict[field] = Label(insert_window,
                                          text="Total hours flying, e.g. 120",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)

        if field == "Email":
          constraints_dict[field] = Label(
              insert_window,
              text="Required: Contact email address, e.g. JohnDoe@gmail.com",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FlightID":
          constraints_dict[field] = Label(
              insert_window,
              text="Select all Flights (IDs) this pilot operates",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)

        # increment y axis
        y += 30

      ## -------------------------------------------------------- Flight table

      if table_name == "Flights":
        aircraft_ids = c.execute('''select AircraftID from Aircrafts''')
        aircraft_ids = [aircraft_id[0] for aircraft_id in aircraft_ids]
        if field == "FlightID":
          entry_dict[field] = Entry(insert_window, bg=pk_bg)
        elif field == "Type":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=flight_type_list)
        elif field == "AircraftID":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=aircraft_ids)
        # listbox for foreign key
        elif field == "PilotID":
          entry_dict[field] = Listbox(insert_window,
                                      selectmode="multiple",
                                      exportselection=False,
                                      bg=junc_bg)

          for pilotID in pilotID_existing:
            entry_dict[field].insert(pilotID_existing.index(pilotID), pilotID)

        else:
          entry_dict[field] = Entry(insert_window)

        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

        # add constraint notes
        if field == "FlightID":
          constraints_dict[field] = Label(
              insert_window,
              text="Primary key: 5-digit code, e.g. DXCU9",
              font=(font, 8, 'bold'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DepartureAirport":
          constraints_dict[field] = Label(
              insert_window,
              text="3-letter airport code, e.g. JFK",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ArrivalAirport":
          constraints_dict[field] = Label(
              insert_window,
              text="3-letter airport code, e.g. JFKh",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "AircraftID":
          constraints_dict[field] = Label(
              insert_window,
              text=
              "Select from saved IDs, insert into Aircrafts table if new aircraft",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FlightDuration":
          constraints_dict[field] = Label(
              insert_window,
              text="Enter in format 'XhXmin' e.g. 3h22m",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DepartureDate":
          constraints_dict[field] = Label(insert_window,
                                          text="YYYY-MM-DD, e.g. 2023-12-31",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DepartureTime":
          constraints_dict[field] = Label(insert_window,
                                          text="HH:MM, e.g. 08:04, 14:55",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ArrivalDate":
          constraints_dict[field] = Label(insert_window,
                                          text="YYYY-MM-DD, e.g. 2023-12-31",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ArrivalTime":
          constraints_dict[field] = Label(insert_window,
                                          text="HH:MM, e.g. 08:04, 14:55",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "PilotID":
          constraints_dict[field] = Label(
              insert_window,
              text="Select all pilots (IDs) this flight is assigned to.",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        # increment y axis
        y += 30

      ## -------------------------------------------------------- Aircraft table

      if table_name == "Aircrafts":
        ### create dropdown boxes for restricted fields
        if field == "AircraftID":
          entry_dict[field] = Entry(insert_window, bg=pk_bg)

        elif field == "Model":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=models_list)
        elif field == "Manufacturer":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=manufacturer_list)
        elif field == "EngineType":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=aircraft_engine_types)
        elif field == "OwnershipType":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=aircraft_ownership_types)
        elif field == "Insured":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=insured)
        else:
          entry_dict[field] = Entry(insert_window)

        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)
        if field == "AircraftID":
          constraints_dict[field] = Label(
              insert_window,
              text="Primary key: 10-digit code, e.g. AA03XYZ678",
              font=(font, 8, 'bold'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "RegistrationNumber":
          constraints_dict[field] = Label(insert_window,
                                          text="8-digit code, e.g. 03XYZ678",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ManufacturingDate":
          constraints_dict[field] = Label(insert_window,
                                          text="YYYY-MM-DD, e.g. 2019-12-31",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "SeatingCapacity":
          constraints_dict[field] = Label(insert_window,
                                          text="Positive Integer, e.g. 250",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FuelCapacity":
          constraints_dict[field] = Label(
              insert_window,
              text="Positive Integer (in gallons), e.g. 78747",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "MaximumDistance":
          constraints_dict[field] = Label(
              insert_window,
              text="In miles, maximum 2 decimals, e.g. 1240.88",
              font=(
                  font,
                  8,
                  'italic',
              ),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)

        # increment y axis
        y += 30

      ## -------------------------------------------------------- Destination table
      if table_name == "Destinations":
        ### create dropdown boxes for restricted fields
        if field == "DestinationID":
          entry_dict[field] = Entry(insert_window, bg=pk_bg)

        elif field == "Country":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=country_list)
        elif field == "Timezone":
          entry_dict[field] = ttk.Combobox(insert_window,
                                           state="readonly",
                                           values=timezones)
        else:
          entry_dict[field] = Entry(insert_window)

        def on_trigger(event):
          entry_dict["DestinationAirport"].delete(0, END)
          ID_value = entry_dict["DestinationID"].get().strip().upper()
          if ID_value in airport_info:
            entry_dict["DestinationAirport"].insert(
                END, string=airport_info[ID_value])
          return

        entry_dict["DestinationID"].bind("<KeyRelease>", on_trigger)
        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

        # add constraint notes
        if field == "DestinationID":
          constraints_dict[field] = Label(
              insert_window,
              text="Primary key: 3-letter airport code, e.g. JFK",
              font=(font, 8, 'bold'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "City":
          constraints_dict[field] = Label(insert_window,
                                          text="City name, e.g. New York",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)

        # increment y axis
        y += 30

    return

  # check [INPUT VALIDITY] for all fields
  def insert_confirm():

    # -----------------PILOTS-------------------#
    if table_dropdown.get() == "Pilots":

      # list of all error messages to display
      error_list = []

      # Unique Primary Key
      c.execute('''select PilotID from Pilots''')
      pilotIDs = c.fetchall()
      key_values = [pilotID[0] for pilotID in pilotIDs]
      if entry_dict["PilotID"].get() in key_values:
        error_list.append(
            f"{len(error_list)+1}. PilotID already exist in record. Primary key cannot have duplicate values."
        )

      if entry_dict["PilotID"].get() == "":
        error_list.append(f"{len(error_list)+1}. PilotID cannot be empty.")

      if not re.match(r'^[a-zA-Z0-9]{6}$', entry_dict['PilotID'].get()):
        error_list.append(
            f"{len(error_list)+1}. PilotID must be 6-digit code consisting of only letters A-Z and numbers 0-9."
        )
      # DateOfBirth, DateHired must be dd/mm/yyyy
      if entry_dict["DateOfBirth"].get() != "" and not re.match(
          r'\d{4}-\d{2}-\d{2}$', entry_dict["DateOfBirth"].get()):
        error_list.append(
            f"{len(error_list)+1}. DateOfBirth must be YYYY-MM-DD format.")

      if entry_dict["DateHired"].get() != "" and not re.match(
          r'\d{4}-\d{2}-\d{2}', entry_dict["DateHired"].get()):
        error_list.append(
            f"{len(error_list)+1}. DateHired must be YYYY-MM-DD format.")

      # Name must be String of text (letters in the alphabet)
      if entry_dict["FirstName"].get() != "" and not re.match(
          r'^[a-zA-Z]+$', entry_dict["FirstName"].get()):
        error_list.append(
            f"{len(error_list)+1}. FirstName must be a String of text (letters in the alphabet)."
        )

      if entry_dict["LastName"].get() != "" and not re.match(
          r'^[a-zA-Z]+$', entry_dict["LastName"].get()):
        error_list.append(
            f"{len(error_list)+1}. LastName must be a String of text (letters in the alphabet)."
        )

      if entry_dict["MiddleName"].get() != "" and not re.match(
          r'^[a-zA-Z]+$', entry_dict["LastName"].get()):
        error_list.append(
            f"{len(error_list)+1}. MiddleName must be a String of text (letters in the alphabet)."
        )

      # LicenseNumber must be 11 digits of Letters and numbers
      if entry_dict["LicenseNumber"].get() != "" and not re.match(
          r'^[a-zA-Z0-9]{11}$', entry_dict["LicenseNumber"].get()):
        error_list.append(
            f"{len(error_list)+1}. LicenseNumber must be 11-digit code consisting of only letters A-Z and numbers 0-9."
        )

      # FlightHours must be an integer
      if entry_dict['FlightHours'].get() != "" and not re.match(
          r'^[0-9]+$', entry_dict['FlightHours'].get()):
        error_list.append(
            f"{len(error_list)}. FlightHours must be a positive integer.")

      # FlightHours must be an integer
      if not re.match(r'^[\w\.-]+@[\w\.-]+$', entry_dict['Email'].get()):
        error_list.append(f"{len(error_list)}. Invalid email address.")
      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=insert_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, insert to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=insert_window,
            title="Confirm Submission",
            message="Please check the data input. Is it correct?")
        if confirm:
          # fetch all input values and insert into Pilot Table
          pilot_id = entry_dict["PilotID"].get().upper()
          email = entry_dict["Email"].get().lower()
          first_name = entry_dict["FirstName"].get().title()
          middle_name = entry_dict["MiddleName"].get().title()
          last_name = entry_dict["LastName"].get().title()
          gender = entry_dict["Gender"].get()
          nationality = entry_dict["Nationality"].get()
          date_of_birth = entry_dict["DateOfBirth"].get()
          license_number = entry_dict["LicenseNumber"].get()
          date_hired = entry_dict["DateHired"].get()

          flight_hours = entry_dict["FlightHours"].get()
          flight_hours = int(flight_hours) if flight_hours != "" else -1
          seniority = entry_dict["Seniority"].get()

          c.execute(
              '''
              INSERT INTO PILOTS VALUES 
              (?, ?, ?, ?, ?, ?, ?, date(?), ?, date(?), ?, ?)
              ''',
              (pilot_id, email, first_name if first_name != "" else None,
               middle_name if middle_name != "" else None, last_name
               if last_name != "" else None, gender if gender != "" else None,
               nationality if nationality != "" else None,
               None if date_of_birth == "" else date_of_birth,
               license_number if license_number != 0 else None,
               None if date_hired == "" else date_hired,
               flight_hours if flight_hours != -1 else None,
               seniority if seniority != "" else None))
          conn.commit()
          # show messagebox confirming insertion
          messagebox.showinfo(parent=insert_window,
                              title="Success",
                              message="Record inserted!")

          # fetch all listbox values and insert to pilot-flight Junction table
          associated_flights = [
              entry_dict['FlightID'].get(index)
              for index in entry_dict['FlightID'].curselection()
          ]
          if len(associated_flights) > 0:
            for flight_id in associated_flights:
              c.execute(f'''
              INSERT INTO Pilot_Flight_JUNC VALUES 
              ('{pilot_id}','{flight_id}')
              ''')
              conn.commit()

    # -----------------Destinations-------------------#
    if table_dropdown.get() == "Destinations":

      # list of all error messages to display
      error_list = []

      # Unique Primary Key
      c.execute('''select DestinationID from Destinations''')
      destinationIDs = c.fetchall()
      key_values = [destinationID[0] for destinationID in destinationIDs]
      if entry_dict["DestinationID"].get() in key_values:
        error_list.append(
            f"{len(error_list)+1}. DestinationID already exist in record. Primary key cannot have duplicate values."
        )

      if entry_dict["DestinationID"].get() == "":
        error_list.append(
            f"{len(error_list)+1}. DestinationID cannot be empty.")

      if not re.match(r'[A-Za-z]{3}', entry_dict['DestinationID'].get()):
        error_list.append(
            f"{len(error_list)+1}. DestinationID must be 3-letter airport code."
        )
      # DateOfBirth, DateHired must be yyyy/mm/dd
      if entry_dict["City"].get() != "" and not re.match(
          r'[A-Za-z\s]+', entry_dict["City"].get()):
        error_list.append(f"{len(error_list)+1}. Invalid city name.")

      if entry_dict["DestinationAirport"].get() != "" and not re.match(
          r"[A-Za-z\s']+", entry_dict["DestinationAirport"].get()):
        error_list.append(f"{len(error_list)+1}. Invalid airport name.")
      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=insert_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, insert to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=insert_window,
            title="Confirm Submission",
            message=
            "Please check that all data inputs are correct. Confirm submission?"
        )

        if confirm:

          # fetch all input values and insert into Pilot Table
          destination_id = entry_dict["DestinationID"].get().upper()
          destination_airport = entry_dict["DestinationAirport"].get().title()
          city = entry_dict["City"].get().title()
          country = entry_dict["Country"].get().title()
          timezone = entry_dict["Timezone"].get()

          c.execute(
              '''
              INSERT INTO DESTINATIONS VALUES 
              (?, ?, ?, ?, ?)
              ''', (destination_id,
                    None if destination_airport == "" else destination_airport,
                    None if city == "" else city,
                    None if country == "" else country,
                    None if timezone == "" else timezone))
          conn.commit()
          # show messagebox confirming insertion
          messagebox.showinfo(parent=insert_window,
                              title="Success",
                              message="Record inserted!")

      # background colour back to white

    # -----------------FLIGHTS------------------#
    if table_dropdown.get() == "Flights":

      # list of all error messages to display
      error_list = []

      # Unique Primary Key
      c.execute('''select FlightID from Flights''')
      flightIDs = c.fetchall()
      key_values = [flightID[0] for flightID in flightIDs]
      if entry_dict["FlightID"].get() in key_values:
        error_list.append(
            f"{len(error_list)+1}. FlightID already exist in record. Primary key cannot have duplicate values."
        )

      if entry_dict["FlightID"].get() == "":
        error_list.append(f"{len(error_list)+1}. FlightID cannot be empty.")

      if not re.match(r'^[a-zA-Z0-9]{5}$', entry_dict['FlightID'].get()):
        error_list.append(
            f"{len(error_list)+1}. FlightID must be 5-digit code consisting of only letters A-Z and numbers 0-9."
        )
      # ADD CHECK FOR FOREIGN KEYS

      # airport code check
      # check foreign key validity for DepartureAirport and ArrivalAirport fields
      c.execute('''select DestinationID from Destinations''')
      destinationIDs = c.fetchall()
      destinationID_existing = [
          destinationID[0] for destinationID in destinationIDs
      ]

      if entry_dict["DepartureAirport"].get() != "" and entry_dict[
          "DepartureAirport"].get() not in destinationID_existing:
        error_list.append(
            f"{len(error_list)+1}. Invalid Departure airport, please add new destination airport before assigning to flight."
        )
      if entry_dict["ArrivalAirport"].get() != "" and entry_dict[
          "ArrivalAirport"].get() not in destinationID_existing:
        error_list.append(
            f"{len(error_list)+1}. Invalid Arrival airport, please add new destination airport before assigning to flight."
        )

      # check foreign key validity for aircraftID field
      c.execute('''select AircraftID from Aircrafts''')
      aircraftIDs = c.fetchall()
      aircraftID_existing = [aircraftID[0] for aircraftID in aircraftIDs]

      if entry_dict["AircraftID"].get() != "" and entry_dict["AircraftID"].get(
      ) not in aircraftID_existing:
        error_list.append(
            f"{len(error_list)+1}. Invalid AirportID, please add aircraft before assigning to flight."
        )
      # Name must be String of text (letters in the alphabet)
      if entry_dict["FlightDuration"].get() != "" and not re.match(
          r'^\d{1,2}h\d{1,2}m$', entry_dict["FlightDuration"].get()):
        error_list.append(
            f"{len(error_list)+1}. Flight duration must be in 'xxhxxm' format, e.g. 08h55m."
        )

      if entry_dict["DepartureDate"].get() != "" and not re.match(
          r'^\d{4}-\d{2}-\d{2}$', entry_dict["DepartureDate"].get()):
        error_list.append(
            f"{len(error_list)+1}. DepartureDate must be in 'YYYY-MM-DD' format."
        )

      if entry_dict["DepartureTime"].get() != "" and not re.match(
          r'^(?:[01]\d|2[0-3]):[0-5]\d$', entry_dict["DepartureTime"].get()):
        error_list.append(
            f"{len(error_list)+1}. DepartureTime must be in 'HH:MM' format.")

      if entry_dict["ArrivalDate"].get() != "" and not re.match(
          r'^\d{4}-\d{2}-\d{2}$', entry_dict["ArrivalDate"].get()):
        error_list.append(
            f"{len(error_list)+1}. ArrivalDate must be in 'YYYY-MM-DD' format."
        )

      if entry_dict["ArrivalTime"].get() != "" and not re.match(
          r'^(?:[01]\d|2[0-3]):[0-5]\d$', entry_dict["ArrivalTime"].get()):
        error_list.append(
            f"{len(error_list)+1}. ArrivalTime must be in 'HH:MM' format.")

      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=insert_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, insert to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=insert_window,
            title="Confirm Submission",
            message=
            "Please check that all data inputs are correct. Confirm submission?"
        )
        if confirm:
          # fetch all input values and insert into Pilot Table
          flight_id = entry_dict["FlightID"].get().upper()
          departure_airport = entry_dict["DepartureAirport"].get().upper()
          arrival_airport = entry_dict["ArrivalAirport"].get().upper()
          aircraft_id = entry_dict["AircraftID"].get().upper()
          if entry_dict["FlightDuration"].get() != '':
            flight_duration_h = int(
                entry_dict["FlightDuration"].get().split("h")[0])
            flight_duration_m = int(entry_dict["FlightDuration"].get()[-3:-1])
            flight_duration = flight_duration_h * 60 + flight_duration_m
          else:
            flight_duration = -1

          departure_date = entry_dict["DepartureDate"].get()
          arrival_date = entry_dict["ArrivalDate"].get()

          if entry_dict['DepartureTime'] != '':
            departure_time = entry_dict['DepartureTime'].get() + ":00"
          else:
            departure_time = ''

          if entry_dict['ArrivalTime'] != '':
            arrival_time = entry_dict['ArrivalTime'].get() + ":00"
          else:
            arrival_time = ''

          type = entry_dict["Type"].get()

          c.execute(
              '''
              INSERT INTO FLIGHTS VALUES 
              (?, ?, ?, ?, ?, date(?), time(?), date(?), time(?), ?)
              ''', (flight_id,
                    None if departure_airport == "" else departure_airport,
                    None if arrival_airport == "" else arrival_airport,
                    None if aircraft_id == "" else aircraft_id,
                    None if flight_duration == -1 else flight_duration,
                    None if departure_date == "" else departure_date,
                    None if departure_time == "" else departure_time,
                    None if arrival_date == "" else arrival_date,
                    None if arrival_time == "" else arrival_time,
                    None if type == "" else type))

          conn.commit()
          # show messagebox confirming insertion
          messagebox.showinfo(parent=insert_window,
                              title="Success",
                              message="Record inserted!")

          # fetch all listbox values and insert to pilot-flight Junction table
          associated_pilots = [
              entry_dict['PilotID'].get(index)
              for index in entry_dict['PilotID'].curselection()
          ]

          if len(associated_pilots) > 0:
            for pilot_id in associated_pilots:
              c.execute(f'''
              INSERT INTO Pilot_Flight_JUNC VALUES 
              ('{pilot_id}','{flight_id}')
              ''')
              conn.commit()

    # -----------------AIRCRAFTS------------------#

    if table_dropdown.get() == "Aircrafts":

      # list of all error messages to display
      error_list = []

      # Unique Primary Key
      c.execute('''select AircraftID from Aircrafts''')
      aircraftIDs = c.fetchall()
      key_values = [aircraftID[0] for aircraftID in aircraftIDs]
      if entry_dict["AircraftID"].get() in key_values:
        error_list.append(
            f"{len(error_list)+1}. AircraftID already exist in record. Primary key cannot have duplicate values."
        )

      if entry_dict["AircraftID"].get() == "":
        error_list.append(f"{len(error_list)+1}. AircraftID cannot be empty.")

      if not re.match(r'^[a-zA-Z0-9]{10}$', entry_dict['AircraftID'].get()):
        error_list.append(
            f"{len(error_list)+1}. AircraftID must be 10-digit code consisting of only letters A-Z and numbers 0-9."
        )

      # Other fields check
      if entry_dict["RegistrationNumber"].get() != "" and not re.match(
          r'^[a-zA-Z0-9]{8}$', entry_dict["RegistrationNumber"].get()):
        error_list.append(
            f"{len(error_list)+1}. RegistrationNumber must be 10-digit code consisting of only letters A-Z and numbers 0-9."
        )

      if entry_dict["ManufacturingDate"].get() != "" and not re.match(
          r'^\d{4}-\d{2}-\d{2}$', entry_dict["ManufacturingDate"].get()):
        error_list.append(
            f"{len(error_list)+1}. ManufacturingDate must be in 'YYYY-MM-DD' format."
        )

      if entry_dict["SeatingCapacity"].get() != "" and not re.match(
          r'^(?:[1-9]\d{0,2}|900)$', entry_dict["SeatingCapacity"].get()):
        error_list.append(
            f"{len(error_list)+1}. SeatingCapacity must be an integer in range 1-900."
        )

      if entry_dict["FuelCapacity"].get() != "" and not re.match(
          r'^(?:[1-9]\d{0,4}|100000)$', entry_dict["SeatingCapacity"].get()):
        error_list.append(
            f"{len(error_list)+1}. SeatingCapacity must be an integer in range 1-100,000."
        )

      if entry_dict["MaximumDistance"].get() != "" and not re.match(
          r'^(?:(?:[1-9]\d*|0)(?:\.\d{1,2})?)$',
          entry_dict["MaximumDistance"].get()):
        error_list.append(
            f"{len(error_list)+1}. MaximumDistance must be a positive number with maximum 2 decimals."
        )

      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=insert_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, insert to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=insert_window,
            title="Confirm Submission",
            message=
            "Please check that all data inputs are correct. Confirm submission?"
        )
        if confirm:
          # fetch all input values and insert into Pilot Table
          aircraft_id = entry_dict["AircraftID"].get().upper()
          model = entry_dict["Model"].get()
          registration_number = entry_dict["RegistrationNumber"].get().upper()
          manufacturer = entry_dict["Manufacturer"].get()
          manufacturing_date = entry_dict["ManufacturingDate"].get()
          seating_capacity = int(entry_dict["SeatingCapacity"].get(
          )) if entry_dict["SeatingCapacity"].get() != "" else -1
          engine_type = entry_dict["EngineType"].get()
          fuel_capacity = int(entry_dict["FuelCapacity"].get(
          )) if entry_dict["FuelCapacity"].get() != "" else -1
          maximum_distance = float(entry_dict["MaximumDistance"].get(
          )) if entry_dict["MaximumDistance"].get() != "" else -1
          ownership_type = entry_dict["OwnershipType"].get()
          insured = entry_dict["Insured"].get()

          c.execute(
              '''
              INSERT INTO AIRCRAFTS VALUES 
              (?, ?, ?, ?, date(?), ?, ?, ?, ?, ?, ?)
              ''', (aircraft_id, None if model == "" else model,
                    None if registration_number == "" else registration_number,
                    None if manufacturer == "" else manufacturer,
                    None if manufacturing_date == "" else manufacturing_date,
                    None if seating_capacity == -1 else seating_capacity,
                    None if engine_type == "" else engine_type,
                    None if fuel_capacity == -1 else fuel_capacity,
                    None if maximum_distance == -1 else maximum_distance,
                    None if ownership_type == "" else ownership_type,
                    None if insured == "" else insured))
          conn.commit()
          # show messagebox confirming insertion
          messagebox.showinfo(parent=insert_window,
                              title="Success",
                              message="Record inserted!")

    return

  # add event listener to dropdown list
  table_dropdown.bind("<<ComboboxSelected>>", show_fields_textbox)

  # add confirm button
  confirm_button = Button(insert_window,
                          text="Confirm",
                          command=insert_confirm)
  confirm_button.place(relx=0.92, rely=0.70, x=0, y=0, anchor=SE)

  # add table viewer button
  viewer_button = Button(insert_window,
                         text="Table Viewer",
                         command=table_viewer,
                         height=1)
  viewer_button.place(x=350, y=18)

  conn.commit()

  return


# ---------------------------------SEARCH----------------------------------#
def search():

  # call heading generator
  search_window, table_dropdown = menu_heading(master, "Search")
  # assign new window and dropdown list by calling heading generator
  label_dict = {}
  entry_dict = {}
  foreign_label = []

  complex = ""
  fields = []
  condition_selected_state = IntVar()
  operator_selected_state = IntVar()

  complex_label = Label(search_window,
                        text="Customised condition:",
                        font=(font, 10, 'bold'),
                        fg="darkgreen")
  complex_entry = Entry(search_window, width=25)
  complex_label_instruction = Label(
      search_window,
      text="Enter customised conditions: WHERE...",
      font=(font, 8, 'italic'),
      fg="darkgreen")
  complex_example_ln1 = Label(
      search_window,
      text="e.g., (fieldA == 'x' and fieldB in ('B','C'))",
      font=(font, 8, 'bold'),
      fg="darkred")
  complex_example_ln2 = Label(
      search_window,
      text="OR (fieldC in (SELECT DISTINCT fieldX in Table Y)",
      font=(font, 8, 'bold'),
      fg="darkred")

  # function to generate list of fields and input boxes (for conditions)
  def show_fields_textbox(event):
    # Get the selected table name and all field names
    table_name = table_dropdown.get()
    c.execute(f"SELECT * FROM {table_name}")
    fields = [description[0] for description in c.description]
    if table_name == "Pilots":
      fields.append("FlightID")
    if table_name == "Flights":
      fields.append("PilotID")
      fields.remove("DepartureDateTime")
      fields.remove("ArrivalDateTime")

    # Create heading for "Field Name" and "Condition"
    field_name_label = Label(search_window,
                             text="Select type:",
                             font=(font, 10, 'bold'),
                             fg='darkgreen')
    field_name_label.place(x=20, y=70)
    condition_label = Label(search_window,
                            text="Joined Condition(s)",
                            font=(font, 10, 'bold'),
                            fg='darkgreen')
    condition_label.place(x=150, y=70)
    instruction_label = Label(search_window,
                              text="Enter below individual field conditions.",
                              font=(font, 8, 'italic'),
                              fg='darkgreen')
    instruction_label.place(x=150, y=100)
    example_label = Label(search_window,
                          text="in the form of partial SQL statements.",
                          font=(font, 8, 'italic'),
                          fg='darkgreen')
    example_label.place(x=150, y=120)
    example_label2 = Label(search_window,
                           text="e.g., =000001, in ('JFK','LAX'), >=500",
                           font=(font, 8, 'bold'),
                           fg='darkred')
    example_label2.place(x=150, y=140)
    example_label.place(x=150, y=120)
    # Create separate inputbox for customised condition

    or_label = Label(search_window,
                     text="OR",
                     font=(font, 10, 'bold'),
                     fg='darkgreen').place(x=410, y=70)

    complex_label.place(x=490, y=70)

    complex_example_ln1.place(x=490, y=115)
    complex_example_ln2.place(x=520, y=130)

    complex_entry.place(x=490, y=170, height=140)

    complex_label_instruction.place(x=490, y=93)

    #Radiobuttons for condition type
    #Variable to hold on to which radio button value is checked.

    def condition_radio_used():
      return condition_selected_state.get()

    condition_selected_state.set(1)
    field_wise = Radiobutton(search_window,
                             text="",
                             value=1,
                             variable=condition_selected_state,
                             command=condition_radio_used).place(x=121, y=68)
    customised = Radiobutton(search_window,
                             text="",
                             value=2,
                             variable=condition_selected_state,
                             command=condition_radio_used).place(x=460, y=68)

    #Radiobuttons for condition type
    #Variable to hold on to which radio button value is checked.

    def operator_radio_used():
      return operator_selected_state.get()

    operator_selected_state.set(1)
    operator_label = Label(search_window,
                           text="Logical operator:",
                           font=(font, 9, 'italic'),
                           fg='blue').place(x=20, y=170)
    AND = Radiobutton(search_window,
                      text="AND",
                      fg='blue',
                      value=1,
                      variable=operator_selected_state,
                      command=operator_radio_used).place(x=145, y=170)
    OR = Radiobutton(search_window,
                     text="OR",
                     fg='blue',
                     value=2,
                     variable=operator_selected_state,
                     command=operator_radio_used).place(x=210, y=170)

    # delete existing labels and entryboxes
    for label in label_dict.values():
      label.destroy()
    for entry in entry_dict.values():
      entry.destroy()
    for label in foreign_label:
      label.destroy()
    label_dict.clear()
    entry_dict.clear()
    foreign_label.clear()

    # set starting axis for first label
    x = 20
    y = 200

    # add new labels and entryboxes
    for field in fields:

      if table_name == "Pilots" and field == "FlightID":
        label_foreign_key = Label(
            search_window,
            text="Search by associated FlightIDs, comma-delimited if multiple",
            font=(font, 8, 'italic'),
            fg="darkred")
        label_foreign_key.place(x=x + 130, y=y + 4)

        label_foreign_key_example = Label(
            search_window,
            text="e.g. 'AAA80', 'KMY88', 'CZW39'",
            font=(font, 8, 'bold'),
            fg="darkred")
        label_foreign_key_example.place(x=x + 130, y=y + 20)

        foreign_label.append(label_foreign_key)
        foreign_label.append(label_foreign_key_example)

        label_dict[field] = Label(search_window,
                                  text=field,
                                  font=(font, 9, 'bold'))

        entry_dict[field] = Entry(search_window, width=30, bg=junc_bg)

        label_dict[field].place(x=x, y=y + 40)
        entry_dict[field].place(x=x + 130, y=y + 40)

      elif table_name == "Flights" and field == "PilotID":

        label_foreign_key = Label(
            search_window,
            text="Search by associated PilotIDs, comma-delimited if multiple",
            font=(font, 8, 'italic'),
            fg="darkred")
        label_foreign_key.place(x=x + 130, y=y + 4)

        label_foreign_key_example = Label(
            search_window,
            text="e.g. '000001', '000002', '000003'",
            font=(font, 8, 'bold'),
            fg="darkred")
        label_foreign_key_example.place(x=x + 130, y=y + 20)

        foreign_label.append(label_foreign_key)
        foreign_label.append(label_foreign_key_example)

        label_dict[field] = Label(search_window,
                                  text=field,
                                  font=(font, 9, 'bold'))
        entry_dict[field] = Entry(search_window, width=30, bg=junc_bg)

        label_dict[field].place(x=x, y=y + 40)
        entry_dict[field].place(x=x + 130, y=y + 40)

      else:
        label_dict[field] = Label(search_window, text=field)
        entry_dict[field] = Entry(search_window, width=25)

        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

      y += 30
    return

  # fetch query, check for error and run search
  def search_confirm():
    # if no table is selected, show error message
    if table_dropdown.get() == "Please select":
      messagebox.showinfo("Error", "Please select a table.")
      return

    else:

      # field-wise search

      # fetch operator from radiobutton value
      operator = ""
      if int(condition_selected_state.get()) == 1:
        if int(operator_selected_state.get()) == 1:
          operator = "AND"
        if int(operator_selected_state.get()) == 2:
          operator = "OR"

        # get all field names of table selected and store in list fields
        table_name = table_dropdown.get()
        c.execute(f"SELECT * FROM {table_name}")
        fields = [description[0] for description in c.description]
        if table_name == "Flights":
          fields.remove("DepartureDateTime")
          fields.remove(
              "ArrivalDateTime"
          )  # DepartureDateTime ArrivalDateTime are derived field of Flights

        # initialise string for sql query
        condition_string = ""

        # check if fields have conditions populated
        no_condition = True
        for field in fields:
          if entry_dict[field].get() != "":
            no_condition = False
        # if no conditions populated -- condition_string = ""
        if no_condition:
          pass

        # if conditions exist
        else:
          field_wise_conditions = []
          condition_string = ""
          for field in fields:
            if entry_dict[field].get() != "":
              field_wise_conditions.append(field + " " +
                                           entry_dict[field].get())
          for i in range(len(field_wise_conditions)):
            field_wise_conditions[i] = field_wise_conditions[i].strip()
            if i != len(field_wise_conditions) - 1:
              condition_string += "(" + field_wise_conditions[
                  i] + ")" + f" {operator} "
            else:
              condition_string += "(" + field_wise_conditions[i] + ")"
          condition_string = "WHERE (" + condition_string + ")"  # WHERE ((field1 = value1) AND (field2 = value2)...)

          # if foreign key (saved in Junction table) was a condition
          # create function to build subquery in the junction table, for extracting primary key values

        def build_place_holder(table_name):
          delimiters = r', |\s'
          foreign_key = "FlightID" if table_name == "Pilots" else "PilotID"
          primary_key = "FlightID" if table_name == "Flights" else "PilotID"

          foreign_keys = re.split(delimiters, entry_dict[foreign_key].get())

          sql_placeholder_list = ", ".join(foreign_keys)

          sql_placeholder_subquery = f"SELECT {primary_key} FROM Pilot_Flight_JUNC WHERE {foreign_key} IN ({sql_placeholder_list})"

          return sql_placeholder_subquery

        # if searching Pilots table and Flights table (with many-to-many relationships)
        sql_placeholder_subquery = ""
        if (table_name == "Pilots" and entry_dict["FlightID"].get() != "") or (
            table_name == "Flights" and entry_dict["PilotID"].get() != ""):
          sql_placeholder_subquery = build_place_holder(table_name)

        # Conditionally generate SQL query
        # create var primary_key for subquery formulation
        primary_key = ""
        if table_name == "Pilots":
          primary_key = "PilotID"
        if table_name == "Flights":
          primary_key = "FlightID"

        sql_query = ""
        if condition_string != "":  # if no conditions specified in fields
          if sql_placeholder_subquery != "":  # if subquery in junction table exists
            #    (must be one of Pilots or Flights) table)
            # join subquery with condition_string
            if operator == "AND":
              sql_query = f"SELECT * FROM {table_name} {condition_string} AND {primary_key} in ({sql_placeholder_subquery})"
            if operator == "OR":
              sql_query = f"SELECT * FROM {table_name} {condition_string} OR {primary_key} in ({sql_placeholder_subquery})"
          else:
            sql_query = f"SELECT * FROM {table_name} {condition_string}"
        else:
          if sql_placeholder_subquery != "":
            sql_query = f"SELECT * FROM {table_name} WHERE {primary_key} in ({sql_placeholder_subquery})"
          else:
            sql_query = f"SELECT * FROM {table_name}"

          # create table view
        try:
          table_viewer_window = Toplevel(search_window)
          table_viewer_window.minsize(width=800, height=500)

          c.execute(sql_query)
          records = c.fetchall()
          columns = tuple([description[0] for description in c.description])
          table_view = ttk.Treeview(table_viewer_window,
                                    columns=columns,
                                    show="headings")
          for column in columns:
            table_view.column(width=120, column=column)
          for i in range(len(columns)):
            table_view.heading(columns[i], text=columns[i])
          table_view.pack()
          for obs in records:
            table_view.insert('', 'end', values=obs)
          # get the count of rows retrieved and show in view title
          c.execute(f"SELECT count(*) FROM ({sql_query})")
          row_count = c.fetchone()[0]
          table_viewer_window.title(
              f"{table_dropdown.get()} Search View: {row_count} observations found"
          )

        # if error occur
        except:
          messagebox.showerror(
              "Error",
              "Invalid WHERE Condition, please check for syntax and try again.",
              parent=search_window)

      # Customised search
      if int(condition_selected_state.get()) == 2:
        # if no condition pecified
        if complex_entry.get() == "":

          table_viewer_window = Toplevel(search_window)
          table_viewer_window.minsize(width=600, height=500)

          table_viewer_window.title(f"{table_dropdown.get()} Search View")
          c.execute(f"SELECT * FROM {table_dropdown.get()}")

          records = c.fetchall()
          columns = tuple([description[0] for description in c.description])
          table_view = ttk.Treeview(table_viewer_window,
                                    columns=columns,
                                    show="headings")
          for column in columns:
            table_view.column(width=120, column=column)
          for i in range(len(columns)):
            table_view.heading(columns[i], text=columns[i])
          table_view.pack()
          for obs in records:
            table_view.insert('', 'end', values=obs)

          # get the count of rows retrieved and show in view title
          c.execute(f"SELECT count(*) FROM {table_dropdown.get()}")
          row_count = c.fetchone()[0]
          table_viewer_window.title(
              f"{table_dropdown.get()} Search View: {row_count} observations found"
          )

        else:
          try:
            condition = complex_entry.get()
            table_viewer_window = Toplevel(search_window)
            table_viewer_window.maxsize(width=800, height=500)
            c.execute(
                f"SELECT count(*) FROM {table_dropdown.get()} WHERE {condition}"
            )
            row_count = c.fetchone()[0]
            table_viewer_window.title(
                f"{table_dropdown.get()} Search View: {row_count} observations found"
            )
            c.execute(
                f"SELECT * FROM {table_dropdown.get()} where ({condition})")
            records = c.fetchall()
            columns = tuple([description[0] for description in c.description])
            table_view = ttk.Treeview(table_viewer_window,
                                      columns=columns,
                                      show="headings")
            for column in columns:
              table_view.column(width=120, column=column)
            for i in range(len(columns)):
              table_view.heading(columns[i], text=columns[i])
            table_view.pack()
            for obs in records:
              table_view.insert('', 'end', values=obs)
          except:
            messagebox.showerror(
                "Error",
                "Invalid Condition, please check for syntax and try again.",
                parent=search_window)

    # declare table viewer function for table viewer button
  def table_viewer():
    # table viewer window
    if table_dropdown.get() == "Please select":
      messagebox.showerror("Error",
                           "Please select a table",
                           parent=search_window)
      return

    table_viewer_window = Toplevel(search_window)
    table_viewer_window.maxsize(width=800, height=500)
    table_viewer_window.title(f"{table_dropdown.get()} Records")
    c.execute(f"SELECT * FROM {table_dropdown.get()}")
    records = c.fetchall()
    columns = tuple([description[0] for description in c.description])
    table_view = ttk.Treeview(table_viewer_window,
                              columns=columns,
                              show="headings")
    for column in columns:
      table_view.column(width=120, column=column)
    for i in range(len(columns)):
      table_view.heading(columns[i], text=columns[i])
    table_view.pack()
    for obs in records:
      table_view.insert('', 'end', values=obs)
    # get the count of rows retrieved and show in view title
    c.execute(f"SELECT count(*) FROM {table_dropdown.get()}")
    row_count = c.fetchone()[0]
    table_viewer_window.title(
        f"{table_dropdown.get()} Search View: {row_count} observations found")

    return

  # create table viewer button
  viewer_button = Button(search_window,
                         text="Table Viewer",
                         command=table_viewer,
                         height=1)
  viewer_button.place(x=350, y=18)

  # add event listener to dropdown list
  table_dropdown.bind("<<ComboboxSelected>>", show_fields_textbox)

  # add confirm button
  confirm_button = Button(search_window,
                          text="Search and View",
                          command=search_confirm)
  confirm_button.place(relx=0.92, rely=0.70, x=0, y=0, anchor=SE)
  conn.commit()

  return


# ---------------------------------DELETE----------------------------------#
def delete():
  table_viewer_window = None
  delimiters = r', |\s'
  # call heading generator
  delete_window, table_dropdown = menu_heading(master, "delete")
  # assign new window and dropdown list by calling heading generator
  label_dict = {}
  entry_dict = {}
  foreign_label = []
  complex = ""
  fields = []
  condition_selected_state = IntVar()
  operator_selected_state = IntVar()

  # initialise sql_query variable to store conditional select query
  sql_query = ""

  complex_label = Label(delete_window,
                        text="Delete by Customised condition:",
                        font=(font, 10, 'bold'),
                        fg="darkgreen")
  complex_entry = Entry(delete_window, width=25)
  complex_label_instruction = Label(
      delete_window,
      text="Enter customised conditions (subqueries allowed).",
      font=(font, 8, 'italic'),
      fg="darkgreen")
  complex_example_ln1 = Label(
      delete_window,
      text="e.g., (fieldA == 'x' and fieldB in ('B','C'))",
      font=(font, 8, 'bold'),
      fg="darkred")
  complex_example_ln2 = Label(
      delete_window,
      text="OR (fieldC in (SELECT DISTINCT fieldX in Table Y)",
      font=(font, 8, 'bold'),
      fg="darkred")

  # function to generate list of fields and input boxes (for conditions)
  def show_fields_textbox(event):

    # Get the selected table name and all field names
    table_name = table_dropdown.get()
    c.execute(f"SELECT * FROM {table_name}")
    fields = [description[0] for description in c.description]
    if table_name == "Pilots":
      fields.append("FlightID")
    if table_name == "Flights":
      fields.append("PilotID")
      fields.remove("DepartureDateTime")
      fields.remove("ArrivalDateTime")

    # Create heading for "Field Name" and "Condition"
    field_name_label = Label(delete_window,
                             text="Select type:",
                             font=(font, 10, 'bold'),
                             fg='darkgreen')
    field_name_label.place(x=20, y=70)
    condition_label = Label(delete_window,
                            text="Delete by Joined Condition(s)",
                            font=(font, 10, 'bold'),
                            fg='darkgreen')
    condition_label.place(x=150, y=70)
    instruction_label = Label(delete_window,
                              text="Enter below individual field conditions.",
                              font=(font, 8, 'italic'),
                              fg='darkgreen')
    instruction_label.place(x=150, y=100)
    example_label = Label(delete_window,
                          text="in the form of partial SQL statements.",
                          font=(font, 8, 'italic'),
                          fg='darkgreen')
    example_label.place(x=150, y=120)
    example_label2 = Label(delete_window,
                           text="e.g., =000001, in ('JFK','LAX'), >=500",
                           font=(font, 8, 'bold'),
                           fg='darkred')
    example_label2.place(x=150, y=140)

    # Create separate inputbox for customised condition

    or_label = Label(delete_window,
                     text="OR",
                     font=(font, 10, 'bold'),
                     fg='darkgreen').place(x=410, y=70)

    complex_label.place(x=490, y=70)
    complex_example_ln1.place(x=490, y=115)
    complex_example_ln2.place(x=520, y=130)

    complex_entry.place(x=490, y=155, height=140)

    complex_label_instruction.place(x=490, y=93)

    #Radiobuttons for condition type
    #Variable to hold on to which radio button value is checked.

    def condition_radio_used():
      return condition_selected_state.get()

    condition_selected_state.set(1)
    field_wise = Radiobutton(delete_window,
                             text="",
                             value=1,
                             variable=condition_selected_state,
                             command=condition_radio_used).place(x=121, y=68)
    customised = Radiobutton(delete_window,
                             text="",
                             value=2,
                             variable=condition_selected_state,
                             command=condition_radio_used).place(x=460, y=68)

    #Radiobuttons for condition type
    #Variable to hold on to which radio button value is checked.

    def operator_radio_used():
      return operator_selected_state.get()

    operator_selected_state.set(1)
    operator_label = Label(delete_window,
                           text="Logical operator:",
                           font=(font, 9, 'italic'),
                           fg='blue').place(x=20, y=170)
    AND = Radiobutton(delete_window,
                      text="AND",
                      fg='blue',
                      value=1,
                      variable=operator_selected_state,
                      command=operator_radio_used).place(x=145, y=170)
    OR = Radiobutton(delete_window,
                     text="OR",
                     fg='blue',
                     value=2,
                     variable=operator_selected_state,
                     command=operator_radio_used).place(x=210, y=170)

    # delete existing labels and entryboxes

    for label in label_dict.values():
      label.destroy()

    for entry in entry_dict.values():
      entry.destroy()

    for label in foreign_label:
      label.destroy()

    # set starting axis for first label
    x = 20
    y = 200

    # add new labels and entryboxes
    for field in fields:

      if table_name == "Pilots" and field == "FlightID":
        label_foreign_key = Label(
            delete_window,
            text="Delete by associated FlightIDs, comma-delimited if multiple",
            font=(font, 8, 'italic'),
            fg="darkred")
        label_foreign_key.place(x=x + 130, y=y + 4)

        label_foreign_key_example = Label(
            delete_window,
            text="e.g. 'AAA80', 'KMY88', 'CZW39'",
            font=(font, 8, 'bold'),
            fg="darkred")
        label_foreign_key_example.place(x=x + 130, y=y + 20)

        foreign_label.append(label_foreign_key)
        foreign_label.append(label_foreign_key_example)

        label_dict[field] = Label(delete_window,
                                  text=field,
                                  font=(font, 9, 'bold'))

        entry_dict[field] = Entry(delete_window, width=30, bg=junc_bg)

        label_dict[field].place(x=x, y=y + 40)
        entry_dict[field].place(x=x + 130, y=y + 40)

      elif table_name == "Flights" and field == "PilotID":

        label_foreign_key = Label(
            delete_window,
            text="Delete by associated PilotIDs, comma-delimited if multiple",
            font=(font, 8, 'italic'),
            fg="darkred")
        label_foreign_key.place(x=x + 130, y=y + 4)

        label_foreign_key_example = Label(
            delete_window,
            text="e.g. '000001', '000002', '000003'",
            font=(font, 8, 'bold'),
            fg="darkred")
        label_foreign_key_example.place(x=x + 130, y=y + 20)

        foreign_label.append(label_foreign_key)
        foreign_label.append(label_foreign_key_example)

        label_dict[field] = Label(delete_window,
                                  text=field,
                                  font=(font, 9, 'bold'))
        entry_dict[field] = Entry(delete_window, width=30, bg=junc_bg)

        label_dict[field].place(x=x, y=y + 40)
        entry_dict[field].place(x=x + 130, y=y + 40)

      else:
        label_dict[field] = Label(delete_window, text=field)
        entry_dict[field] = Entry(delete_window, width=25)

        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

      y += 30

    return

  # fetch query, check for error and run delete
  def delete_view():

    # declare confirm_delete_in_view function
    def confirm_delete():

      # if table=Flights, then any records deleted should also be deleted from the Junction table

      junc_delete_query = ""
      delete_query = sql_query.replace('SELECT *', 'DELETE')

      if table_dropdown.get() == "Flights":
        junc_delete_query = f'''DELETE FROM PILOT_FLIGHT_JUNC 
                                       WHERE FLIGHTID IN 
                                                      (SELECT FLIGHTID FROM ({sql_query})) '''

      try:
        if table_dropdown.get() == "Flights":
          c.execute(junc_delete_query)
          conn.commit()
        c.execute(delete_query)
        # all tables except flights potentially have values that are foreign key in 'flights'
      except:
        messagebox.showerror(
            parent=delete_window,
            title='Error',
            message=
            'Foreign key constraint failed. The records you selected contain foreign key values in another table.'
        )
      else:
        conn.commit()
        messagebox.showinfo(parent=delete_window,
                            title='Success',
                            message='Record deleted successfully.')
      finally:
        table_viewer_window.destroy()
      return

    # if no table is selected, show error message
    if table_dropdown.get() == "Please select":
      messagebox.showinfo("Error", "Please select a table.")
      return

    else:

      # field-wise delete

      # fetch operator from radiobutton value
      operator = ""
      if int(condition_selected_state.get()) == 1:
        if int(operator_selected_state.get()) == 1:
          operator = "AND"
        if int(operator_selected_state.get()) == 2:
          operator = "OR"

        # get all field names of table selected and store in list fields
        table_name = table_dropdown.get()
        c.execute(f"SELECT * FROM {table_name}")
        fields = [description[0] for description in c.description]
        if table_name == "Flights":
          fields.remove("DepartureDateTime")
          fields.remove("ArrivalDateTime")

        # initialise string for sql query
        condition_string = ""

        # check if fields have conditions populated
        no_condition = True
        for field in fields:
          if entry_dict[field].get() != "":
            no_condition = False
        # if no conditions populated -- condition_string = ""
        if no_condition:
          pass

        # if conditions exist
        else:
          field_wise_conditions = []
          condition_string = ""
          for field in fields:
            if entry_dict[field].get() != "":
              field_wise_conditions.append(field + " " +
                                           entry_dict[field].get())
          for i in range(len(field_wise_conditions)):
            field_wise_conditions[i] = field_wise_conditions[i].strip()
            if i != len(field_wise_conditions) - 1:
              condition_string += "(" + field_wise_conditions[
                  i] + ")" + f" {operator} "
            else:
              condition_string += "(" + field_wise_conditions[i] + ")"
          condition_string = "WHERE " + condition_string  # WHERE ((field1 = value1) AND (field2 = value2)...)

          # if foreign key (saved in Junctino table) was a condition
          # create function to build subquery in the junction table, for extracting primary key values

        def build_place_holder(table_name):

          foreign_key = "FlightID" if table_name == "Pilots" else "PilotID"
          primary_key = "FlightID" if table_name == "Flights" else "PilotID"

          foreign_keys = re.split(delimiters, entry_dict[foreign_key].get())

          sql_placeholder_list = ", ".join(foreign_keys)

          sql_placeholder_subquery = f"SELECT {primary_key} FROM Pilot_Flight_JUNC WHERE {foreign_key} IN ({sql_placeholder_list})"

          return sql_placeholder_subquery

        # if deleteing Pilots table and Flights table (with many-to-many relationships)
        sql_placeholder_subquery = ""
        if (table_name == "Pilots" and entry_dict["FlightID"].get() != "") or (
            table_name == "Flights" and entry_dict["PilotID"].get() != ""):
          sql_placeholder_subquery = build_place_holder(table_name)

        # Conditionally generate SQL query
        # create var primary_key for subquery formulation
        primary_key = ""
        if table_name == "Pilots":
          primary_key = "PilotID"
        if table_name == "Flights":
          primary_key = "FlightID"

        if condition_string != "":  # if no conditions specified in fields
          if sql_placeholder_subquery != "":  # if subquery in junction table exists
            #    (must be one of Pilots or Flights) table)
            # join subquery with condition_string
            sql_query = f"SELECT * FROM {table_name} {condition_string} AND {primary_key} in ({sql_placeholder_subquery})"
          else:
            sql_query = f"SELECT * FROM {table_name} {condition_string}"
        else:
          if sql_placeholder_subquery != "":
            sql_query = f"SELECT * FROM {table_name} WHERE {primary_key} in ({sql_placeholder_subquery})"
          else:
            sql_query = f"SELECT * FROM {table_name}"

          # create whole table view
        try:
          c.execute(f"SELECT count(*) FROM ({sql_query})")
          row_count = c.fetchone()[0]
          # execute sql_query to view selected observations
          c.execute(sql_query)
          records = c.fetchall()

          table_viewer_window = Toplevel(delete_window)
          table_viewer_window.minsize(width=800, height=500)

          # add 'confirm delete' button to confirm deletion
          confirm_delete_button = Button(table_viewer_window,
                                         text="Confirm Delete",
                                         font=(font, 9, 'bold'),
                                         fg='red',
                                         command=confirm_delete)
          confirm_delete_button.pack(side=TOP, anchor=NW)

          # get the count of rows retrieved and show in view title

          table_viewer_window.title(
              f"Delete from {table_dropdown.get()}: {row_count} observations found"
          )

          # if no records are found, display message instead of confirm delete button
          if row_count == 0:
            confirm_delete_button.destroy()
            Label(table_viewer_window,
                  text="No records found",
                  font=(font, 9, 'bold'),
                  fg='blue').pack(side=TOP, anchor=NW)

          columns = tuple([description[0] for description in c.description])
          table_view = ttk.Treeview(table_viewer_window,
                                    columns=columns,
                                    show="headings")
          for column in columns:
            table_view.column(width=120, column=column)
          for i in range(len(columns)):
            table_view.heading(columns[i], text=columns[i])
          table_view.pack()
          for obs in records:
            table_view.insert('', 'end', values=obs)

        # if error occur
        except:
          messagebox.showerror(
              "Error",
              "Invalid WHERE Condition, please check for syntax and try again.",
              parent=delete_window)

      # Customised delete
      if int(condition_selected_state.get()) == 2:

        # if no condition pecified
        if complex_entry.get() == "":
          # show view window
          table_viewer_window = Toplevel(delete_window)
          table_viewer_window.minsize(width=600, height=500)
          table_viewer_window.title(f"{table_dropdown.get()} delete View")

          # add 'confirm delete' button to confirm deletion
          confirm_delete_button = Button(table_viewer_window,
                                         text="Confirm Delete",
                                         font=(font, 9, 'bold'),
                                         fg='red',
                                         command=confirm_delete)
          confirm_delete_button.pack(side=TOP, anchor=NW)

          # get number of records to show in view title
          c.execute(f"SELECT count(*) FROM {table_dropdown.get()}")
          row_count = c.fetchone()[0]
          table_viewer_window.title(
              f"Delete from {table_dropdown.get()}: {row_count} observations found"
          )

          # set sql_query string
          sql_query = f"SELECT * FROM {table_dropdown.get()}"
          c.execute(sql_query)

          records = c.fetchall()
          columns = tuple([description[0] for description in c.description])
          table_view = ttk.Treeview(table_viewer_window,
                                    columns=columns,
                                    show="headings")
          for column in columns:
            table_view.column(width=120, column=column)
          for i in range(len(columns)):
            table_view.heading(columns[i], text=columns[i])
          table_view.pack()
          for obs in records:
            table_view.insert('', 'end', values=obs)

          # get the count of rows retrieved and show in view title
          c.execute(f"SELECT count(*) FROM {table_dropdown.get()}")
          row_count = c.fetchone()[0]

          table_viewer_window.title(
              f"Delete from {table_dropdown.get()}: {row_count} observations found"
          )
          # if no records are found, display message instead of confirm delete button
          if row_count == 0:
            confirm_delete_button.destroy()
            Label(table_viewer_window,
                  text="No observations found",
                  font=(font, 9, 'bold'),
                  fg='blue').pack(side=TOP, anchor=NW)

        else:
          try:
            condition = complex_entry.get()
            # get number of records to show in view title
            c.execute(
                f"SELECT count(*) FROM {table_dropdown.get()} WHERE {condition}"
            )

            row_count = c.fetchone()[0]

            # set sql_query string and run search filter
            sql_query = f"SELECT * FROM {table_dropdown.get()} WHERE {condition}"
            c.execute(sql_query)
            records = c.fetchall()

            table_viewer_window = Toplevel(delete_window)
            table_viewer_window.maxsize(width=800, height=500)

            # add 'confirm delete' button to confirm deletion
            confirm_delete_button = Button(table_viewer_window,
                                           text="Confirm Delete",
                                           font=(font, 9, 'bold'),
                                           fg='red',
                                           command=confirm_delete)
            confirm_delete_button.pack(side=TOP, anchor=NW)

            table_viewer_window.title(
                f"Delete from {table_dropdown.get()}: {row_count} observations found"
            )
            # if no records are found, display message instead of confirm delete button
            if row_count == 0:
              confirm_delete_button.destroy()
              Label(table_viewer_window,
                    text="No observations found",
                    font=(font, 9, 'bold'),
                    fg='blue').pack(side=TOP, anchor=NW)

            columns = tuple([description[0] for description in c.description])
            table_view = ttk.Treeview(table_viewer_window,
                                      columns=columns,
                                      show="headings")
            for column in columns:
              table_view.column(width=120, column=column)
            for i in range(len(columns)):
              table_view.heading(columns[i], text=columns[i])
            table_view.pack()
            for obs in records:
              table_view.insert('', 'end', values=obs)
          except:
            messagebox.showerror(
                "Error",
                "Invalid Condition, please check for syntax and try again.",
                parent=delete_window)
    return
    # declare table viewer function for table viewer button
  def table_viewer():
    # table viewer window
    if table_dropdown.get() == "Please select":
      messagebox.showerror("Error",
                           "Please select a table",
                           parent=delete_window)
      return

    table_viewer_window = Toplevel(delete_window)
    table_viewer_window.maxsize(width=800, height=500)
    table_viewer_window.title(f"{table_dropdown.get()} Records")
    c.execute(f"SELECT * FROM {table_dropdown.get()}")
    records = c.fetchall()
    columns = tuple([description[0] for description in c.description])
    table_view = ttk.Treeview(table_viewer_window,
                              columns=columns,
                              show="headings")
    for column in columns:
      table_view.column(width=120, column=column)
    for i in range(len(columns)):
      table_view.heading(columns[i], text=columns[i])
    table_view.pack()
    for obs in records:
      table_view.insert('', 'end', values=obs)
    # get the count of rows retrieved and show in view title
    c.execute(f"SELECT count(*) FROM {table_dropdown.get()}")
    row_count = c.fetchone()[0]
    table_viewer_window.title(
        f"Delete from {table_dropdown.get()}: {row_count} observations found")

    return

  # create standard view button in heading
  viewer_button = Button(delete_window,
                         text="Table Viewer",
                         command=table_viewer,
                         height=1)
  viewer_button.place(x=350, y=18)

  # add event listener to dropdown list
  table_dropdown.bind("<<ComboboxSelected>>", show_fields_textbox)

  # add 'View and delete' button to check selected records to delete
  confirm_button = Button(delete_window,
                          text="View and Delete",
                          command=delete_view)
  confirm_button.place(relx=0.92, rely=0.70, x=0, y=0, anchor=SE)
  conn.commit()

  return


# ---------------------------------UPDATE----------------------------------#
def update():

  # assign new window and dropdown list by calling heading generator

  update_window, table_dropdown = menu_heading(master, "update")

  # create empty containers to store field labels and entry boxes
  label_dict = {}
  entry_dict = {}
  constraints_dict = {}
  fields = []

  # add table viewer function
  def table_viewer():
    # table viewer window
    if table_dropdown.get() == "Please select":
      messagebox.showerror("Error",
                           "Please select a table",
                           parent=update_window)
      return

    table_viewer_window = Toplevel(update_window)
    table_viewer_window.minsize(width=600, height=500)
    table_viewer_window.title(f"{table_dropdown.get()} Records")

    c.execute(f"SELECT * FROM {table_dropdown.get()}")
    records = c.fetchall()
    columns = tuple([description[0] for description in c.description])
    table_view = ttk.Treeview(table_viewer_window,
                              columns=columns,
                              show="headings")
    for column in columns:
      table_view.column(width=120, column=column)

    for i in range(len(columns)):
      table_view.heading(columns[i], text=columns[i])
    table_view.pack()
    for obs in records:
      table_view.insert('', 'end', values=obs)
    # get the count of rows retrieved and show in view title
    c.execute(f"SELECT count(*) FROM {table_dropdown.get()}")
    row_count = c.fetchone()[0]
    table_viewer_window.title(
        f"{table_dropdown.get()} Search View: {row_count} observations found")
    return

  # declare function to show fields and textboxes

  def show_fields_textbox(event):

    # Get the selected table name and all field names
    table_name = table_dropdown.get()
    c.execute(f"SELECT * FROM {table_name}")
    fields = [description[0] for description in c.description]
    if table_name == "Pilots":
      fields.append("FlightID")
    if table_name == "Flights":
      fields.append("PilotID")
      fields.remove("DepartureDateTime")
      fields.remove("ArrivalDateTime")
    # delete existing labels and entryboxes
    for label in label_dict.values():
      label.destroy()
    for entry in entry_dict.values():
      entry.destroy()
    for constraint in constraints_dict.values():
      constraint.destroy()

    label_dict.clear()
    entry_dict.clear()
    constraints_dict.clear()

    # create new labels and entryboxes
    # set axis
    x = 20
    y = 70

    c.execute("SELECT FlightID FROM Flights")
    flightIDs = c.fetchall()
    flightID_existing = [flight[0] for flight in flightIDs]

    c.execute("SELECT PilotID FROM Pilots")
    pilotIDs = c.fetchall()
    pilotID_existing = [pilot[0] for pilot in pilotIDs]

    for field in fields:
      # create label
      label_dict[field] = Label(update_window, text=field)

      # create input box and add constraints
      ## -------------------------------------------------------Pilot table
      if table_name == "Pilots":
        ### create dropdown boxes for restricted fields
        # ALL flightIDs
        if field == "PilotID":
          entry_dict[field] = Entry(update_window, bg=pk_bg)

        elif field == "Gender":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=gender_list)
        elif field == "Nationality":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=nationalities)
        elif field == "Seniority":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=seniorities)
        elif field == "FlightID":
          entry_dict[field] = Listbox(update_window,
                                      selectmode="multiple",
                                      exportselection=False,
                                      bg=junc_bg)

          for flightID in flightID_existing:
            entry_dict[field].insert(flightID_existing.index(flightID),
                                     flightID)
        else:
          entry_dict[field] = Entry(update_window)

        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

        if field == "FirstName":
          constraints_dict[field] = Label(update_window,
                                          text="e.g. William",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "LastName":
          constraints_dict[field] = Label(update_window,
                                          text="e.g. Smith",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "MiddleName":
          constraints_dict[field] = Label(update_window,
                                          text="(Optional)",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DateOfBirth" or field == "DateHired":
          constraints_dict[field] = Label(update_window,
                                          text="YYYY-MM-DD, e.g. 1999-12-31",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "LicenseNumber":
          constraints_dict[field] = Label(
              update_window,
              text="11-digit code, e.g. QWER1234UIO",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FlightHours":
          constraints_dict[field] = Label(update_window,
                                          text="Total hours flying, e.g. 120",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)

        if field == "Email":
          constraints_dict[field] = Label(
              update_window,
              text="Required: Contact email address, e.g. JohnDoe@gmail.com",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FlightID":
          constraints_dict[field] = Label(
              update_window,
              text="Select all Flights (IDs) this pilot operates",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)

        # increment y axis
        y += 30

      ## -------------------------------------------------------- Flight table
      if table_name == "Flights":
        aircraft_ids = c.execute('''select AircraftID from Aircrafts''')
        aircraft_ids = [aircraft_id[0] for aircraft_id in aircraft_ids]

        if field == "FlightID":
          entry_dict[field] = Entry(update_window, bg=pk_bg)

        elif field == "Type":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=flight_type_list)
        elif field == "AircraftID":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=aircraft_ids)
        # listbox for foreign key
        elif field == "PilotID":
          entry_dict[field] = Listbox(update_window,
                                      selectmode="multiple",
                                      exportselection=False,
                                      bg=junc_bg)

          for pilotID in pilotID_existing:
            entry_dict[field].insert(pilotID_existing.index(pilotID), pilotID)

        else:
          entry_dict[field] = Entry(update_window)

        # place label and input box

        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

        # add constraint notes

        if field == "DepartureAirport":
          constraints_dict[field] = Label(
              update_window,
              text="3-letter airport code, e.g. JFK",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ArrivalAirport":
          constraints_dict[field] = Label(
              update_window,
              text="3-letter airport code, e.g. JFKh",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "AircraftID":
          constraints_dict[field] = Label(
              update_window,
              text=
              "Select from saved IDs, insert to Aircrafts table if new aircraft",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FlightDuration":
          constraints_dict[field] = Label(
              update_window,
              text="Enter in format 'XhXmin' e.g. 3h22min",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DepartureDate":
          constraints_dict[field] = Label(update_window,
                                          text="YYYY-MM-DD, e.g. 2023-12-31",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DepartureTime":
          constraints_dict[field] = Label(update_window,
                                          text="HH:MM, e.g. 08:04, 14:55",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ArrivalDate":
          constraints_dict[field] = Label(update_window,
                                          text="YYYY-MM-DD, e.g. 2023-12-31",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ArrivalTime":
          constraints_dict[field] = Label(update_window,
                                          text="HH:MM, e.g. 08:04, 14:55",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "PilotID":
          constraints_dict[field] = Label(
              update_window,
              text="Select all pilots (IDs) this flight is assigned to.",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        # increment y axis
        y += 30

      ## -------------------------------------------------------- Aircraft table

      if table_name == "Aircrafts":
        ### create dropdown boxes for restricted fields
        if field == "AircraftID":
          entry_dict[field] = Entry(update_window, bg=pk_bg)

        elif field == "Model":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=models_list)
        elif field == "Manufacturer":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=manufacturer_list)
        elif field == "EngineType":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=aircraft_engine_types)
        elif field == "OwnershipType":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=aircraft_ownership_types)
        elif field == "Insured":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=insured)
        else:
          entry_dict[field] = Entry(update_window)

        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

        # add constraint notes

        if field == "RegistrationNumber":
          constraints_dict[field] = Label(update_window,
                                          text="8-digit code, e.g. 03XYZ678",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ManufacturingDate":
          constraints_dict[field] = Label(update_window,
                                          text="YYYY-MM-DD, e.g. 2019-12-31",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "SeatingCapacity":
          constraints_dict[field] = Label(update_window,
                                          text="Positive Integer, e.g. 250",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FuelCapacity":
          constraints_dict[field] = Label(
              update_window,
              text="Positive Integer (in gallons), e.g. 78747",
              font=(font, 8, 'italic'),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "MaximumDistance":
          constraints_dict[field] = Label(
              update_window,
              text="In miles, maximum 2 decimals, e.g. 1240.88",
              font=(
                  font,
                  8,
                  'italic',
              ),
              fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)

        # increment y axis
        y += 30

      ## -------------------------------------------------------- Destination table
      if table_name == "Destinations":
        ### create dropdown boxes for restricted fields
        if field == "DestinationID":
          entry_dict[field] = Entry(update_window, bg=pk_bg)

        elif field == "Country":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=country_list)
        elif field == "Timezone":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=timezones)
        else:
          entry_dict[field] = Entry(update_window)

        def on_trigger(event):
          entry_dict["DestinationAirport"].delete(0, END)
          ID_value = entry_dict["DestinationID"].get().strip().upper()
          if ID_value in airport_info:
            entry_dict["DestinationAirport"].insert(
                END, string=airport_info[ID_value])
          return

        entry_dict["DestinationID"].bind("<KeyRelease>", on_trigger)
        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

        # add constraint notes

        if field == "City":
          constraints_dict[field] = Label(update_window,
                                          text="City name, e.g. New York",
                                          font=(font, 8, 'italic'),
                                          fg="gray30")
          constraints_dict[field].place(x=x + 310, y=y)

        # increment y axis
        y += 30

    # add search button next to ID field
    autofill_button = Button(update_window,
                             text="Autofill data",
                             command=autofill_data,
                             bg=pk_bg,
                             font=(font, 9, 'bold')).place(x=350, y=68)

    return

  # check [INPUT VALIDITY] for all fields
  def update_confirm():

    # -----------------PILOTS-------------------#
    if table_dropdown.get() == "Pilots":

      # list of all error messages to display
      error_list = []

      # DateOfBirth, DateHired must be dd/mm/yyyy
      if entry_dict["DateOfBirth"].get() != "" and not re.match(
          r'\d{4}-\d{2}-\d{2}$', entry_dict["DateOfBirth"].get()):
        error_list.append(
            f"{len(error_list)+1}. DateOfBirth must be YYYY-MM-DD format.")

      if entry_dict["DateHired"].get() != "" and not re.match(
          r'\d{4}-\d{2}-\d{2}', entry_dict["DateHired"].get()):
        error_list.append(
            f"{len(error_list)+1}. DateHired must be YYYY-MM-DD format.")

      # Name must be String of text (letters in the alphabet)
      if entry_dict["FirstName"].get() != "" and not re.match(
          r'^[a-zA-Z]+$', entry_dict["FirstName"].get()):
        error_list.append(
            f"{len(error_list)+1}. FirstName must be a String of text (letters in the alphabet)."
        )

      if entry_dict["LastName"].get() != "" and not re.match(
          r'^[a-zA-Z]+$', entry_dict["LastName"].get()):
        error_list.append(
            f"{len(error_list)+1}. LastName must be a String of text (letters in the alphabet)."
        )

      if entry_dict["MiddleName"].get() != "" and not re.match(
          r'^[a-zA-Z]+$', entry_dict["LastName"].get()):
        error_list.append(
            f"{len(error_list)+1}. MiddleName must be a String of text (letters in the alphabet)."
        )

      # LicenseNumber must be 11 digits of Letters and numbers
      if entry_dict["LicenseNumber"].get() != "" and not re.match(
          r'^[a-zA-Z0-9]{11}$', entry_dict["LicenseNumber"].get()):
        error_list.append(
            f"{len(error_list)+1}. LicenseNumber must be 11-digit code consisting of only letters A-Z and numbers 0-9."
        )

      # FlightHours must be an integer
      if entry_dict['FlightHours'].get() != "" and not re.match(
          r'^[0-9]+$', entry_dict['FlightHours'].get()):
        error_list.append(
            f"{len(error_list)}. FlightHours must be a positive integer.")

      # FlightHours must be an integer
      if not re.match(r'^[\w\.-]+@[\w\.-]+$', entry_dict['Email'].get()):
        error_list.append(f"{len(error_list)}. Invalid email address.")
      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=update_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, update to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=update_window,
            title="Confirm Submission",
            message="Please check the data input. Is it correct?")
        if confirm:
          # fetch all input values and update into Pilot Table
          pilot_id = entry_dict["PilotID"].get().upper()
          email = entry_dict["Email"].get().lower()
          first_name = entry_dict["FirstName"].get().title()
          middle_name = entry_dict["MiddleName"].get().title()
          last_name = entry_dict["LastName"].get().title()
          gender = entry_dict["Gender"].get()
          nationality = entry_dict["Nationality"].get()
          date_of_birth = entry_dict["DateOfBirth"].get()
          license_number = entry_dict["LicenseNumber"].get()
          date_hired = entry_dict["DateHired"].get()

          flight_hours = entry_dict["FlightHours"].get()
          flight_hours = int(flight_hours) if flight_hours != "" else -1
          seniority = entry_dict["Seniority"].get()

          c.execute(
              '''
              UPDATE PILOTS
              SET
                  Email = ?,
                  FirstName = ?,
                  MiddleName = ?,
                  LastName = ?,
                  Gender = ?,
                  Nationality = ?,
                  DateOfBirth = date(?),
                  LicenseNumber = ?,
                  DateHired = date(?),
                  FlightHours = ?,
                  Seniority = ?
              WHERE PilotID = ?
              ''',
              (email, first_name if first_name != "" else None,
               middle_name if middle_name != "" else None, last_name
               if last_name != "" else None, gender if gender != "" else None,
               nationality if nationality != "" else None,
               date_of_birth if date_of_birth != "" else None,
               license_number if license_number != 0 else None,
               date_hired if date_hired != "" else None,
               flight_hours if flight_hours != -1 else None,
               seniority if seniority != "" else None, pilot_id))
          conn.commit()
          # show messagebox confirming updateion
          messagebox.showinfo(parent=update_window,
                              title="Success",
                              message="Record updateed!")

          # fetch all listbox values and update to pilot-flight Junction table
          associated_flights = [
              entry_dict['FlightID'].get(index)
              for index in entry_dict['FlightID'].curselection()
          ]

          # first delete all records in junc table
          c.execute(f'''
          DELETE FROM PILOT_FLIGHT_JUNC 
                  WHERE PilotID = '{pilot_id}'
          ''')
          if len(associated_flights) > 0:
            for flight_id in associated_flights:
              c.execute(f'''
              INSERT INTO Pilot_Flight_JUNC VALUES 
              ('{pilot_id}','{flight_id}')
              ''')
              conn.commit()

    # -----------------------------Destinations---------------------------------#
    if table_dropdown.get() == "Destinations":

      # list of all error messages to display
      error_list = []

      # DateOfBirth, DateHired must be yyyy/mm/dd
      if entry_dict["City"].get() != "" and not re.match(
          r'[A-Za-z\s]+', entry_dict["City"].get()):
        error_list.append(f"{len(error_list)+1}. Invalid city name.")

      if entry_dict["DestinationAirport"].get() != "" and not re.match(
          r"[A-Za-z\s']+", entry_dict["DestinationAirport"].get()):
        error_list.append(f"{len(error_list)+1}. Invalid airport name.")
      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=update_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, update to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=update_window,
            title="Confirm Submission",
            message=
            "Please check that all data inputs are correct. Confirm submission?"
        )

        if confirm:

          # fetch all input values and update into Pilot Table
          destination_id = entry_dict["DestinationID"].get().upper()
          destination_airport = entry_dict["DestinationAirport"].get().title()
          city = entry_dict["City"].get().title()
          country = entry_dict["Country"].get().title()
          timezone = entry_dict["Timezone"].get()

          c.execute(
              '''
              UPDATE DESTINATIONS
              SET
                  DestinationAirport = ?,
                  City = ?,
                  Country = ?,
                  Timezone = ?
              WHERE DestinationID = ?
              ''', (None if destination_airport == "" else destination_airport,
                    None if city == "" else city,
                    None if country == "" else country,
                    None if timezone == "" else timezone, destination_id))
          conn.commit()
          # show messagebox confirming updateion
          messagebox.showinfo(parent=update_window,
                              title="Success",
                              message="Record updateed!")

      # background colour back to white

    # -----------------FLIGHTS------------------#
    if table_dropdown.get() == "Flights":

      # list of all error messages to display
      error_list = []

      # ADD CHECK FOR FOREIGN KEYS

      # airport code check
      # check foreign key validity for DepartureAirport and ArrivalAirport fields
      c.execute('''select DestinationID from Destinations''')
      destinationIDs = c.fetchall()
      destinationID_existing = [
          destinationID[0] for destinationID in destinationIDs
      ]

      if entry_dict["DepartureAirport"].get() != "" and entry_dict[
          "DepartureAirport"].get() not in destinationID_existing:
        error_list.append(
            f"{len(error_list)+1}. Invalid Departure airport, please add new destination airport before assigning to flight."
        )
      if entry_dict["ArrivalAirport"].get() != "" and entry_dict[
          "ArrivalAirport"].get() not in destinationID_existing:
        error_list.append(
            f"{len(error_list)+1}. Invalid Arrival airport, please add new destination airport before assigning to flight."
        )

      # check foreign key validity for aircraftID field
      c.execute('''select AircraftID from Aircrafts''')
      aircraftIDs = c.fetchall()
      aircraftID_existing = [aircraftID[0] for aircraftID in aircraftIDs]

      if entry_dict["AircraftID"].get() != "" and entry_dict["AircraftID"].get(
      ) not in aircraftID_existing:
        error_list.append(
            f"{len(error_list)+1}. Invalid AirportID, please add aircraft before assigning to flight."
        )
      # Name must be String of text (letters in the alphabet)
      if entry_dict["FlightDuration"].get() != "" and not re.match(
          r'^\d{1,2}h\d{1,2}m$', entry_dict["FlightDuration"].get()):
        error_list.append(
            f"{len(error_list)+1}. Flight duration must be in 'xxhxxm' format, e.g. 08h55m."
        )

      if entry_dict["DepartureDate"].get() != "" and not re.match(
          r'^\d{4}-\d{2}-\d{2}$', entry_dict["DepartureDate"].get()):
        error_list.append(
            f"{len(error_list)+1}. DepartureDate must be in 'YYYY-MM-DD' format."
        )

      if entry_dict["DepartureTime"].get() != "" and not re.match(
          r'^(?:[01]\d|2[0-3]):[0-5]\d$', entry_dict["DepartureTime"].get()):
        error_list.append(
            f"{len(error_list)+1}. DepartureTime must be in 'HH:MM' format.")

      if entry_dict["ArrivalDate"].get() != "" and not re.match(
          r'^\d{4}-\d{2}-\d{2}$', entry_dict["ArrivalDate"].get()):
        error_list.append(
            f"{len(error_list)+1}. ArrivalDate must be in 'YYYY-MM-DD' format."
        )

      if entry_dict["ArrivalTime"].get() != "" and not re.match(
          r'^(?:[01]\d|2[0-3]):[0-5]\d$', entry_dict["ArrivalTime"].get()):
        error_list.append(
            f"{len(error_list)+1}. ArrivalTime must be in 'HH:MM' format.")

      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=update_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, update to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=update_window,
            title="Confirm Submission",
            message=
            "Please check that all data inputs are correct. Confirm submission?"
        )
        if confirm:
          # fetch all input values and update into Pilot Table
          flight_id = entry_dict["FlightID"].get().upper()
          departure_airport = entry_dict["DepartureAirport"].get().upper()
          arrival_airport = entry_dict["ArrivalAirport"].get().upper()
          aircraft_id = entry_dict["AircraftID"].get().upper()
          if entry_dict["FlightDuration"].get() != '':
            flight_duration_h = int(
                entry_dict["FlightDuration"].get().split("h")[0])
            flight_duration_m = int(entry_dict["FlightDuration"].get()[-3:-1])
            flight_duration = flight_duration_h * 60 + flight_duration_m
          else:
            flight_duration = -1

          departure_date = entry_dict["DepartureDate"].get()
          arrival_date = entry_dict["ArrivalDate"].get()

          if entry_dict['DepartureTime'] != '':
            departure_time = entry_dict['DepartureTime'].get() + ":00"
          else:
            departure_time = ''

          if entry_dict['ArrivalTime'] != '':
            arrival_time = entry_dict['ArrivalTime'].get() + ":00"
          else:
            arrival_time = ''

          type = entry_dict["Type"].get()

          c.execute(
              '''
              UPDATE FLIGHTS
              SET
                  DepartureAirport = ?,
                  ArrivalAirport = ?,
                  AircraftID = ?,
                  FlightDuration = ?,
                  DepartureDate = date(?),
                  DepartureTime = time(?),
                  ArrivalDate = date(?),
                  ArrivalTime = time(?),
                  Type = ?
              WHERE FlightID = ?
              ''', (None if departure_airport == "" else departure_airport,
                    None if arrival_airport == "" else arrival_airport,
                    None if aircraft_id == "" else aircraft_id,
                    None if flight_duration == -1 else flight_duration,
                    None if departure_date == "" else departure_date,
                    None if departure_time == "" else departure_time,
                    None if arrival_date == "" else arrival_date,
                    None if arrival_time == "" else arrival_time,
                    None if type == "" else type, flight_id))

          conn.commit()
          # show messagebox confirming updateion
          messagebox.showinfo(parent=update_window,
                              title="Success",
                              message="Record updated!")

          # fetch all listbox values and update to pilot-flight Junction table
          associated_pilots = [
              entry_dict['PilotID'].get(index)
              for index in entry_dict['PilotID'].curselection()
          ]
          c.execute(f'''
          DELETE FROM PILOT_FLIGHT_JUNC 
                WHERE FlightID == '{flight_id}'
                ''')
          if len(associated_pilots) > 0:
            for pilot_id in associated_pilots:
              c.execute(f'''
              insert INTO Pilot_Flight_JUNC VALUES 
              ('{pilot_id}','{flight_id}')
              ''')
              conn.commit()

    # -----------------AIRCRAFTS------------------#

    if table_dropdown.get() == "Aircrafts":

      # list of all error messages to display
      error_list = []

      # Other fields check
      if entry_dict["RegistrationNumber"].get() != "" and not re.match(
          r'^[a-zA-Z0-9]{8}$', entry_dict["RegistrationNumber"].get()):
        error_list.append(
            f"{len(error_list)+1}. RegistrationNumber must be 10-digit code consisting of only letters A-Z and numbers 0-9."
        )

      if entry_dict["ManufacturingDate"].get() != "" and not re.match(
          r'^\d{4}-\d{2}-\d{2}$', entry_dict["ManufacturingDate"].get()):
        error_list.append(
            f"{len(error_list)+1}. ManufacturingDate must be in 'YYYY-MM-DD' format."
        )

      if entry_dict["SeatingCapacity"].get() != "" and not re.match(
          r'^(?:[1-9]\d{0,2}|900)$', entry_dict["SeatingCapacity"].get()):
        error_list.append(
            f"{len(error_list)+1}. SeatingCapacity must be an integer in range 1-900."
        )

      if entry_dict["FuelCapacity"].get() != "" and not re.match(
          r'^(?:[1-9]\d{0,4}|100000)$', entry_dict["SeatingCapacity"].get()):
        error_list.append(
            f"{len(error_list)+1}. FuelCapacity must be an integer in range 1-100,000."
        )

      if entry_dict["MaximumDistance"].get() != "" and not re.match(
          r'^(?:(?:[1-9]\d*|0)(?:\.\d{1,2})?)$',
          entry_dict["MaximumDistance"].get()):
        error_list.append(
            f"{len(error_list)+1}. MaximumDistance must be a positive number with maximum 2 decimals."
        )

      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=update_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, update to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=update_window,
            title="Confirm Submission",
            message=
            "Please check that all data inputs are correct. Confirm submission?"
        )
        if confirm:
          # fetch all input values and update to Pilot Table
          aircraft_id = entry_dict["AircraftID"].get().upper()
          model = entry_dict["Model"].get()
          registration_number = entry_dict["RegistrationNumber"].get().upper()
          manufacturer = entry_dict["Manufacturer"].get()
          manufacturing_date = entry_dict["ManufacturingDate"].get()
          seating_capacity = int(entry_dict["SeatingCapacity"].get(
          )) if entry_dict["SeatingCapacity"].get() != "" else -1
          engine_type = entry_dict["EngineType"].get()
          fuel_capacity = int(entry_dict["FuelCapacity"].get(
          )) if entry_dict["FuelCapacity"].get() != "" else -1
          maximum_distance = float(entry_dict["MaximumDistance"].get(
          )) if entry_dict["MaximumDistance"].get() != "" else -1
          ownership_type = entry_dict["OwnershipType"].get()
          insured = entry_dict["Insured"].get()

          c.execute(
              '''
            UPDATE AIRCRAFTS
            SET
                Model = ?,
                RegistrationNumber = ?,
                Manufacturer = ?,
                ManufacturingDate = date(?),
                SeatingCapacity = ?,
                EngineType = ?,
                FuelCapacity = ?,
                MaximumDistance = ?,
                OwnershipType = ?,
                Insured = ?
            WHERE AircraftID = ?
            ''',
              (None if model == "" else model,
               None if registration_number == "" else registration_number,
               None if manufacturer == "" else manufacturer,
               None if manufacturing_date == "" else manufacturing_date,
               None if seating_capacity == -1 else seating_capacity,
               None if engine_type == "" else engine_type,
               None if fuel_capacity == -1 else fuel_capacity,
               None if maximum_distance == -1 else maximum_distance,
               None if ownership_type == "" else ownership_type,
               None if insured == "" else insured, aircraft_id, aircraft_id))

          conn.commit()
          # show messagebox confirming updateion
          messagebox.showinfo(parent=update_window,
                              title="Success",
                              message="Record updateed!")

    return

  # declare autofill function to retrieve data of particular ID
  def autofill_data():
    table_ID_dict = {
        'Pilots': 'PilotID',
        'Aircrafts': 'AircraftID',
        'Flights': 'FlightID',
        'Destinations': 'DestinationID'
    }
    foreign_key_dict = {'Pilots': 'FlightID', 'Flights': 'PilotID'}

    # query table and retrieve record with matching ID
    table_name = table_dropdown.get()
    id_value = entry_dict[table_ID_dict[table_name]].get()
    find_obs_query = f"select * from {table_name} where {table_ID_dict[table_name]} == '{id_value}'"
    c.execute(find_obs_query)
    obs = c.fetchall()

    # if no records are found
    if len(obs) == 0:
      messagebox.showinfo(parent=update_window,
                          title="Error",
                          message="ID Record not found!")

    # if records match
    else:
      # get list of columns names
      column_list = [description[0] for description in c.description]
      if table_name == "Flights":
        column_list.remove("ArrivalDateTime")
        column_list.remove("DepartureDateTime")
      # if from table flights or pilots - import listbox values from junction table
      listbox_selection = []
      if table_name == "Flights" or table_name == "Pilots":

        junc_table_query = f"select distinct {foreign_key_dict[table_name]} from pilot_flight_junc where {table_ID_dict[table_name]} == '{id_value.upper()}'"
        c.execute(junc_table_query)
        listbox_selection = [val[0] for val in c.fetchall()]

      # get record found
      obs = obs[0]

      # clear values of all entries / comboboxes / listboxes
      for key in entry_dict:
        if isinstance(entry_dict[key], Entry):
          entry_dict[key].delete(0, END)
        if isinstance(entry_dict[key], ttk.Combobox):
          entry_dict[key].set('')
        if isinstance(entry_dict[key], Listbox):
          entry_dict[key].selection_clear(0, END)

      # number of fields shown on screen is +1 for Flights and Pilots tables (foreign key)
      if table_name == "Flights" or table_name == "Pilots":
        field_num = len(column_list) + 1
      else:
        field_num = len(column_list)

      for i in range(field_num):  # i is index of column (0, 1, 2, ...)
        key = ""
        if i < len(column_list):
          key = column_list[i]
          if isinstance(entry_dict[key], Entry):
            if obs[i] != None:
              if key == "DepartureTime" or key == "ArrivalTime":
                datetimestring = obs[i][:-3]
                entry_dict[key].insert(END, datetimestring)
              else:
                entry_dict[key].insert(END, obs[i])
            else:
              entry_dict[key].insert(END, '')
          if isinstance(entry_dict[key], ttk.Combobox):
            if obs[i] is not None:

              values_list = list(entry_dict[key]['values'])
              entry_dict[key][
                  'values'] = values_list  # Optional: Update the values in case they changed

              entry_dict[key].set(values_list[values_list.index(obs[i])])

            else:
              entry_dict[key].set('')

        # select listbox values if from table flights or pilots
        if (table_name == "Flights" or table_name == "Pilots") and isinstance(
            entry_dict[foreign_key_dict[table_name]], Listbox):

          listbox_index = [
              entry_dict[foreign_key_dict[table_name]].get(0, END).index(val)
              for val in listbox_selection
          ]

          # select the associated items in listbox
          for index in listbox_index:
            entry_dict[foreign_key_dict[table_name]].select_set(index)

    return

    # add event listener to dropdown list

  table_dropdown.bind("<<ComboboxSelected>>", show_fields_textbox)

  # add confirm button
  confirm_button = Button(update_window,
                          text="Confirm",
                          command=update_confirm)
  confirm_button.place(relx=0.92, rely=0.70, x=0, y=0, anchor=SE)

  # add table viewer button
  viewer_button = Button(update_window,
                         text="Table Viewer",
                         command=table_viewer,
                         height=1)
  viewer_button.place(x=350, y=18)

  conn.commit()

  return


# -------------------------------Starting Page--------------------------------#
# Create Starting page labels
## welcome prompt
welcome_prompt = Label(master,
                       text="Welcome to the Flight Database Management UI",
                       font=(font, 15),
                       padx=20,
                       pady=20)
welcome_prompt.place(x=20, y=20)

## menu prompt
menu_prompt = Label(master,
                    text="Please select from one of the following:",
                    font=(font, 12),
                    padx=20,
                    pady=20)
menu_prompt.place(x=20, y=65)

# Menu buttons
insert_button = Button(master,
                       text="Insert New Records",
                       font=(font, button_font_size),
                       width=23,
                       padx=5,
                       pady=5,
                       command=insert,
                       bg=main_button_color)
search_button = Button(master,
                       text="Search / View Records",
                       font=(font, button_font_size),
                       width=23,
                       padx=5,
                       pady=5,
                       command=search,
                       bg=main_button_color)
update_button = Button(master,
                       text="Update Existing Records",
                       font=(font, button_font_size),
                       width=23,
                       padx=5,
                       pady=5,
                       command=update,
                       bg=main_button_color)
delete_button = Button(master,
                       text="Delete Records",
                       font=(font, button_font_size),
                       width=23,
                       padx=5,
                       pady=5,
                       command=delete,
                       bg=main_button_color)

# Menu buttons layout
insert_button.place(x=50, y=140)
search_button.place(x=50, y=190)
update_button.place(x=50, y=240)
delete_button.place(x=50, y=290)

# E-R Diagram button
stats_button = Button(master,
                      text="Flight \nSummaries",
                      font=(font, 10),
                      height=10,
                      width=10,
                      padx=5,
                      pady=5,
                      command=flight_stats,
                      bg="deepskyblue1")
stats_button.place(x=285, y=140)

# E-R Diagram button
ER_button = Button(master,
                   text="E-R \nDiagram",
                   font=(font, 10),
                   height=10,
                   width=10,
                   padx=5,
                   pady=5,
                   command=ER_diagram,
                   bg="aquamarine1")
ER_button.place(x=415, y=140)

# commit changes to database
conn.commit()
# run app
master.mainloop()
# close sqlite3 connection
conn.close()

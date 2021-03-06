from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from sys import exit
from numpy.core.numeric import full
from pydicom.filereader import dcmread
import os
# Python program to create 
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog

# Function for opening the 
# file explorer window
def browseSourceDirectory():
	filename = filedialog.askdirectory(initialdir = "",title = "Select Source DICOM directory")
	label_source.configure(text="Source: "+filename)
    # Change label contents
	window.source_path=filename
def browseDestinationDirectory():
	filename = filedialog.askdirectory(initialdir = "",title = "Select Source DICOM directory")
	label_destination.configure(text="Destination: "+filename)
    # Change label contents
	window.destination_path=filename
	
def process():
    
    source_path=window.source_path
    destination_path=window.destination_path
    modality=entry_modality.get()
    #print(modality)
    institution="01"
    #print('strarted')
    total_files=len(os.listdir(source_path))
    #exit()
    file_counter=1
    for path in os.listdir(source_path):
        print('processing file ',file_counter, 'of ',total_files)
        file_counter=file_counter+1
        full_path = os.path.join(source_path, path)
        if os.path.isfile(full_path):
            filename=full_path
            if filename.endswith(".dcm"):                 
                        try:
                            ds=dcmread(filename)
                            #print(ds.ViewPosition,ds.ImageLaterality)
                            #exit()
                            #print('dcm file was read')
                            if(ds.Modality==modality):
                                if ds.InstitutionName != None:
                                    oinstitution=ds.InstitutionName
                                else:
                                    oinstitution="No institution"
                                institution=oinstitution[0]+oinstitution[-1]
                                patient_name="PAT_"+institution+"_"+str(ds.PatientID).zfill(6)
                                #print(patient_name)
                                pat=os.path.join(destination_path,patient_name)
                                #print('patient path was',pat)   
                                try:
                                                                 
                                    #no_of_files=len([name for name in os.listdir(pat) if os.path.isfile(name)])
                                    ##print(no_of_files)
                                    os.makedirs(pat)
                                    #print('dir was created')
                                except OSError as e:
                                    if os.listdir(pat) == []: 
                                        print("No files found in the directory.") 
                                    #else: 
                                        #print(os.listdir(pat))
                                        #print("Some files found in the directory.") 
                                        #raise
                                #exit()
                                ds.PatientName=patient_name
                                
                                ds.InstitutionName=institution
                                #print(patient_name," was processed")
                                ##print(ds.InstitutionName)
                                i=0
                                patf=os.path.join(pat,str(i).zfill(2)+"-"+ds.ViewPosition+"-"+ds.ImageLaterality+".dcm")
                                #print(patf)
                                while(os.path.isfile(patf)):
                                    #print('duplicate files was found for ',patf)
                                    i=i+1
                                    patf=os.path.join(pat,str(i).zfill(2)+"-"+ds.ViewPosition+"-"+ds.ImageLaterality+".dcm")
    
                                ##print(patf)
                                try:
                                    ds.save_as(patf, write_like_original=False)
                                except OSError as e:
                                    print(e.strerror)
                            else:
                                print("No mammo for patient") 
                        except OSError as e:
                            print("Error occurred",e.strerror)
    label_status.configure(text="Status: Finished")
    #print('finished')
    exit
																								
# Create the root window
window = Tk()

# Set window title
window.title('Dicom Cleaner by AIC - R&D')
#window.wm_iconbitmap('aic.ico')

# Set window size
window.geometry("450x300")

#Set window background color
window.config(background = "white")

# Create a File Explorer label
label_source = Label(window, 
							text = "Source: ",
							width=30,
                            justify=LEFT,
							fg = "blue")


label_destination = Label(window, 
							text = "Destination: ",
							width=30,
                            justify=LEFT,
							fg = "blue")
label_sequence = Label(window, 
							text = "Patient Sequence: ",
                            width=20,
                            justify=RIGHT)
label_modality = Label(window, 
							text = "Modality: ",
                            width=20,
                            justify=RIGHT)

label_status = Label(window, 
							text = "Status: ",
							width=20,
                            justify=RIGHT,
							fg = "blue")

button_source = Button(window, 
						text = "Source",
                        width=20,
                        justify=RIGHT,
						command = browseSourceDirectory) 
button_destination = Button(window, 
						text = "Destination",
                        width=20,
                        justify=RIGHT,
						command = browseDestinationDirectory) 
entry_seq=ttk.Entry(window,width=10, justify=LEFT)
entry_modality= ttk.Combobox(window, 
                            values=["MG", "DX"],
                            width=10,
                            justify=LEFT)
entry_modality.current(0)
button_process = Button(window, 
					text = "Process",
                    width=30,
                    justify=LEFT,
					command = process) 

# Grid method is chosen for placing
# the widgets at respective positions 
# in a table like structure by
# specifying rows and columns

#col 1
label_source.grid(column = 2, row = 1, padx=10,pady=10)
label_destination.grid(column = 2, row = 2, padx=10,pady=10)
label_sequence.grid(column = 1, row = 3, padx=10,pady=10)
label_modality.grid(column = 1, row = 4, padx=10,pady=10)
label_status.grid(column = 1, row = 5, padx=10,pady=10)

#col2
button_source.grid(column = 1, row = 1, padx=10,pady=10)
button_destination.grid(column = 1, row = 2, padx=10,pady=10)
entry_seq.grid(column = 2,row = 3, padx=10,pady=10)
entry_modality.grid(column = 2,row = 4, padx=10,pady=10)
button_process.grid(column = 2,row = 5, padx=10,pady=10)
# Let the window wait for any events
window.mainloop()

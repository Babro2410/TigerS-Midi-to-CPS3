from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from tkinter.font import BOLD
from tkinter import ttk
from mido import Message, MidiFile, MidiTrack, tempo2bpm
from textwrap import wrap
import binascii
from mido.midifiles.meta import MetaMessage, MetaSpec, add_meta_spec
import ast
from decimal import *

Yellow_Sulphur = "#f9f0c8"
Light_Brown_Drab = "#be9f9e"
Dark_Olive_Slate = "#37404f"
Blue_Salvia = "#a4b3cf"
Font_UI = "Century Gothic"

#Tkinter design stuff, don't bother.

root = Tk()
root.title("TigerS - Midi to CPS3 music convertor - V.Alpha.0.53 29/04/2022") #Title of the window
root.geometry("520x450") #Window size
root.config(background= Dark_Olive_Slate) #window config
root.resizable(0, 0) #can't resize window
RawConverted_Text = Entry(root) #empty entry so it get's replaced every cycle
root.iconbitmap(default='Resources/546967657253.Babro') #importing images
Other_entry = Entry(root, state='readonly',width="30", bg=Light_Brown_Drab, fg=Light_Brown_Drab, highlightbackground=Light_Brown_Drab )
Other_entry.place(relx = 0.27, rely = 0.18, anchor = CENTER)

ID_instrument_items_HFTF=['Acoustic Guitar', 'Action note', 'Bass', 'Bassoon', 'Bongo percussion', 'Bongos solo', 'Brass', 'Choir', 'Choir 2', 'Clarinet', 'Classic Guitar', 'Classic Guitar 2', 'Closed Cymbal', 'Closed Cymbal 2', 'Cowbell', 'Cymbal', 'DJ Scratch', 'Downlifter', 'Dramatic Brass', 'Drumkit', 'Drumkit (2013)', 'Fantasia', 'Fantasia 2', 'Fantasia 3', 'GBA Square synth', 'Gothic Organ', 'Gothic Organ 2', 'Guitar','Harpsichord', 'Hi-Hat(Closed)', 'Jingle bells', 'Jotaro Guitar', 'Mizmar (Arabic flute)', 'Muffled Analog Kick', 'Muffled rock guitar', 'Organ', 'Percussion', 'Petshop Guitar', 'Petshop Guitar 2', 'Piano', 'Reverse Cymbal', 'Ride', 'Rock Guitar', 'Shaker', 'Shovel', 'Snare', 'Snare 2', 'Snowsteps', 'Synth Bass', 'Timpani', 'Timpani 2', 'Triangle', 'Triangle 2', 'Trombone', 'Trombone 2 (deeper)', 'Trumpet', 'Tuba', 'Vibe', 'Vibraslap', 'Viola Strings', 'Violin Strings', 'Zip Zap']

ID_instrument_List_HFTF= { #INSTRUMENT MAPPING HFTF

    "Drumkit":0,
    "Drumkit (2013)":1,
    "Muffled Analog Kick":2,
    "Snare":3,
    "Snare 2":4,
    "Closed Cymbal":5,
    "Percussion":6,
    "Closed Cymbal 2":7,
    "Cymbal":8,
    "Hi-Hat(Closed)":9,
    "Cowbell":10,
    "Shaker":11,
    "Action note":12,
    "Zip Zap":13,
    "Timpani":14,
    "Ride":15,
    "Bass":16,
    "Synth Bass":17,
    "Acoustic Guitar":18,
    "Rock Guitar":19,
    "Jotaro Guitar":20,
    "Muffled rock guitar":21,
    "Guitar":22,
    "Piano":23,
    "Fantasia":24,
    "Gothic Organ":25,
    "Fantasia 2":26,
    "Fantasia 3":27,
    "Gothic Organ 2":28,
    "Harpsichord":29,
    "Vibe":30,
    "Brass":31,
    "Trumpet":32,
    "Trombone":33,
    "Trombone 2 (deeper)":34,
    "Tuba":35,
    "GBA Square synth":36,
    "Violin Strings":37,
    "Viola Strings":38,
    "Shovel":39,
    "Timpani 2":40,
    "Jingle bells":41,
    "Snowsteps":42,
    "DJ Scratch":43,
    "Dramatic Brass":44,
    "Mizmar (Arabic flute)":45,
    "Choir":46,
    "Choir 2":47,
    "Bongos solo":48,
    "Clarinet":49,
    "Classic Guitar":50,
    "Classic Guitar 2":51,
    "Bongo percussion":52,
    "Petshop Guitar":53,
    "Petshop Guitar 2":54,
    "Bassoon":55,
    "Organ":56,
    "Triangle":57,
    "Triangle 2":58,
    "Reverse Cymbal":59,
    "Downlifter":60,
    "Vibraslap":61
}

ID_instrument_items_RED=['00', '01', '03', '04', '06', '07', '08', '09', '0A', '0B', '0D', '0E', '0F', '10', '11', '13', '14', '17', '18', '1A', '1F', '24', '26', '28', '29', '30', '30', '31', '31', '32', '32', 'Acoustic Bass', 'Bass', 'Brass', 'Brass', 'Bright Piano', 'Choir', 'Choir', 'Cymbal', 'Distortion Guitar', 'Flute', 'Gong', 'Orchestra Hit', 'Organ 1', 'Organ 2', 'Overdrive Guitar', 'Piano', 'Plucked Bass', 'Shakuhachi', 'Shakuhachi', 'Shamisen', 'Shamisen', 'Strings1', 'Strings2', 'Synth Pad1', 'Synth Pad2', 'Synth Pad2', 'Synth Piano', 'Triangle', 'Whistle']

ID_instrument_List_RED={
    "00":0,
    "01":1,
    "Cymbal":2,
    "03":3,
    "04":4,
    "Gong":5,
    "06":6,
    "07":7,
    "08":8,
    "09":9,
    "0A":10,
    "0B":11,
    "Triangle":12,
    "0D":13,
    "0E":14,
    "0F":15,
    "10":16,
    "11":17,
    "Orchestra Hit":18,
    "13":19,
    "14":20,
    "Plucked Bass":21,
    "Bass":22,
    "17":23,
    "18":24,
    "Acoustic Bass":25,
    "1A":26,
    "Distortion Guitar":27,
    "Overdrive Guitar":28,
    "Strings1":29,
    "Strings2":30,
    "1F":31,
    "Piano":32,
    "Bright Piano":33,
    "Synth Piano":34,
    "Organ 1":35,
    "24":36,
    "Organ 2":37,
    "26":38,
    "Brass":39,
    "28":40,
    "29":41,
    "Flute":42,
    "Brass":43,
    "Whistle":44,
    "Synth Pad1":45,
    "Synth Pad2":46,
    "Choir":47,
    "30":48,
    "31":49,
    "32":50,
    "Shamisen":51,
    "Shakuhachi":52,

}

ID_instrument_items_3S=['0B', '0C', '0E', '0F', '10', '11', '1E', '22', '23', '24', 'Beats', 'Breakbeat', 'Choir', 'Church Organ', 'Circuit', 'Cowbell', 'Crystal', 'Cymbal', 'Distortion Guidar', 'Drum', 'Funk Guitar', 'Funk Guitar Pluck', 'Funk Organ', 'Ibuki’s instrument', 'Intro  Breakbeat', 'Loud tone', 'Orchestra Hit', 'Orchestra Hit', 'Percussion', 'Percussion2', 'Percussion3', 'Piano', 'Plucked Bass', 'Sawtooth wave', 'Saxaphone 2', 'Saxophone 1', 'Shakuhachi', 'Softer tone', 'Square Wave', 'Steel Drum', 'Sticks', 'Strings', 'Synth Bass 1', 'Synth Bass 2', 'Synth Bass 3', 'Synth Bass 4', 'Synth Bass 5', 'Synth Bass 6', 'Synth Bass 7', 'Synth Bass 8', 'Synth Pad', 'Synth Slap Bass', 'Synth pluck1', 'Synth pluck2', 'Synth pluck3', 'Synth pluck4', 'Synth pluck5', 'Synth pluck6', 'Taiko Drum', 'Trangle Wave', 'Voice', 'We await your return, warrior', 'Xylopohone']

ID_instrument_List_3S={
    "Percussion":0,
    "Percussion2":1,
    "Cymbal":2,
    "Percussion3":3,
    "Drum":4,
    "Breakbeat":5,
    "Circuit":6,
    "Intro  Breakbeat":7,
    "Voice":8,
    "We await your return, warrior":9,
    "Taiko Drum":10,
    "0B":11,
    "0C":12,
    "Steel Drum":13,
    "0E":14,
    "0F":15,
    "10":16,
    "11":17,
    "Cowbell":18,
    "Trangle Wave":19,
    "Plucked Bass":20,
    "Xylopohone":21,
    "Distortion Guidar":22,
    "Funk Guitar":23,
    "Synth pluck1":24,
    "Synth pluck2":25,
    "Synth pluck3":26,
    "Synth pluck4":27,
    "Synth pluck5":28,
    "Synth pluck6":29,
    "1E":30,
    "Funk Organ":31,
    "Synth Slap Bass":32,
    "Square Wave":33,
    "22":34,
    "23":35,
    "24":36,
    "Saxophone 1":37,
    "Saxaphone 2":38,
    "Piano":39,
    "Ibuki’s instrument":40,
    "Church Organ":41,
    "Loud tone":42,
    "Softer tone":43,
    "Sawtooth wave":44,
    "Choir":45,
    "Strings":46,
    "Shakuhachi":47,
    "Crystal":48,
    "Synth Bass 1":49,
    "Synth Bass 2":50,
    "Synth Bass 3":51,
    "Synth Bass 4":52,
    "Synth Bass 5":53,
    "Synth Bass 6":54,
    "Synth Bass 7":55,
    "Synth Bass 8":56,
    "Synth Pad":57,
    "Sticks":58,
    "Beats":59,
    "Orchestra Hit":60,
    "Funk Guitar Pluck":61,
    "Orchestra Hit":62
}    
def Intrument_Groups ():
    Intrument_Groups.ID_instrument_items= ID_instrument_items_HFTF
    Intrument_Groups.ID_instrument_List = ID_instrument_List_HFTF

Intrument_Groups ()

Data = [] #Data that's then exported at the end.

Drumkit_Default = [['0D'],['03'],['2b'],['2b'],['07'],['02'],['07'],['0a'],['00'],['01'],['07'],['04'],['03'],['03'],['06'],['05'],['06'],['05'],['0e'],['08'],['0e'],['0e'],['08'],['0e'],['0f'],['09'],['09'],['08'],['3b'],['0a'],['08'],['3d'],['0f'],['30'],['30'],['34'],['34'],['34'],['28'],['28'],['1A'],['1A'],['2a'],['09'],['0c'],['0c'],['3d'],['3d'],['00'],['00'],['00'],['2E'],['2E'],['3a'],['39'],['2a'],['29'],['29'],['00'],['06'],['06']]

global Delta_data_list
Delta_data_list = []

class Track_Information_lookup:
    
    Track_0_OG_Track_name = "N/A"
    Track_1_OG_Track_name = "N/A"
    Track_2_OG_Track_name = "N/A"
    Track_3_OG_Track_name = "N/A"
    Track_4_OG_Track_name = "N/A"
    Track_5_OG_Track_name = "N/A"
    Track_6_OG_Track_name = "N/A"
    Track_7_OG_Track_name = "N/A"
    Track_8_OG_Track_name = "N/A"
    Track_9_OG_Track_name = "N/A"
    Track_10_OG_Track_name = "N/A"
    Track_11_OG_Track_name = "N/A"
    Track_12_OG_Track_name = "N/A"
    Track_13_OG_Track_name = "N/A"
    Track_14_OG_Track_name = "N/A"
    Track_15_OG_Track_name = "N/A"

    Track_0_OG_Intrument = "N/A"
    Track_1_OG_Intrument = "N/A"
    Track_2_OG_Intrument = "N/A"
    Track_3_OG_Intrument = "N/A"
    Track_4_OG_Intrument = "N/A"
    Track_5_OG_Intrument = "N/A"
    Track_6_OG_Intrument = "N/A"
    Track_7_OG_Intrument = "N/A"
    Track_8_OG_Intrument = "N/A"
    Track_9_OG_Intrument = "N/A"
    Track_10_OG_Intrument = "N/A"
    Track_11_OG_Intrument = "N/A"
    Track_12_OG_Intrument = "N/A"
    Track_13_OG_Intrument = "N/A"
    Track_14_OG_Intrument = "N/A"
    Track_15_OG_Intrument = "N/A"





def List_Useless_remover(Input,Type): #removes the useless things from a list, only keeps the string data.
    if Type == 1 :
        Input = (str(Input)).replace("[", "").replace("]", "")
        return Input
    if Type == 2 :
        Input = (str(Input)).replace(";", "")
        return Input
    if Type == 3 :
        Input = (str(Input)).replace("[", "").replace("]", "").replace("'", "").replace(", ", "\n")
        return Input
    if Type == 4 :
        Input = (str(Input)).replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace(" ", "")
        return Input
    if Type == 5 :
        Input = (str(Input)).replace("[", "").replace("]", "").replace("'", "").replace(" ","")
        return Input     

def Val_to_var_length (i,n): # N 0 FOR REGULAR, N 1 FOR CPS3
    global Delta_data_list
    Bin_i = (bin(i)[2:])
    if len (bin(i)[2:]) < 8:
        a = hex(i)[2:].zfill(2)
        if len (str(a)) != 2:
                print ("2 bytes delta error")
                print(str(a))
                messagebox.showerror(title="Val_to_var_length error! (ERROR ID:1)", message="Val_to_var_length error! output was not a 2 bytes Delta time")
                raise Exception("Val_to_var_length error")
        Delta_data_list.append(str(a)) 
        return str(a)
    elif 15> len (bin(i)[2:]) > 7:
        a = hex(int((Bin_i[-7:]), 2))[2:].zfill(2)
        b = hex(128+int((Bin_i[:-7]),2))[2:].zfill(2)
        if n == 0 : #Regular
            Delta_data_list.append(str(b)+str(a))
            if len (str(b)+str(a)) != 4:
                print ("4 bytes delta error")
                print(str(b))
                print(str(a))
                messagebox.showerror(title="Val_to_var_length error! (ERROR ID:2)", message="Val_to_var_length error! output was not a 4 bytes Delta time")
                raise Exception("Val_to_var_length error") 
            return str(b)+str(a)
        elif n == 1 : #CPS3 Delta:
            b = hex(int((Bin_i[:-7]),2))[2:].zfill(2)
            if len (str(b)+str(a)) != 4:
                print ("4 bytes delta error")
                print(str(b))
                print(str(a))
                messagebox.showerror(title="Val_to_var_length error! (ERROR ID:3)", message="Val_to_var_length error! output was not a 4 bytes Delta time")
                raise Exception("Val_to_var_length error")
            Delta_data_list.append(str(b)+str(a)) 
            return str(b)+str(a)
    elif 22> len (bin(i)[2:]) >14 :
        a = hex(int((Bin_i[-7:]), 2))[2:].zfill(2)
        b = hex(128+int((Bin_i[-14:-7]),2))[2:].zfill(2)
        c = hex(128+int((Bin_i[:-14:]),2))[2:].zfill(2)
        if n == 0 : #Regular
            Delta_data_list.append(str(c)+str(b)+str(a))
            if len (str(c)+str(b)+str(a)) != 6:
                print ("6 bytes delta error")
                print(str(c))
                print(str(b))
                print(str(a))
                messagebox.showerror(title="Val_to_var_length error! (ERROR ID:4)", message="Val_to_var_length error! output was not a 6 bytes Delta time")
                raise Exception("Val_to_var_length error") 
            return str(c)+str(b)+str(a)
        elif n == 1 : #CPS3 Delta:
            b = hex(int((Bin_i[-14:-7]),2))[2:].zfill(2)
            c = hex(int((Bin_i[:-14:]),2))[2:].zfill(2)
            Delta_data_list.append(str(c)+str(b)+str(a))
            if len (str(c)+str(b)+str(a)) != 6:
                print ("6 bytes delta error")
                print(str(c))
                print(str(b))
                print(str(a))
                messagebox.showerror(title="Val_to_var_length error! (ERROR ID:5)", message="Val_to_var_length error! output was not a 6 bytes Delta time")
                raise Exception("Val_to_var_length error")
            return str(c)+str(b)+str(a)        

def Var_Length_to_Val (i,n): # N 0 FOR REGULAR, N 1 FOR CPS3
   i = i.replace(" ","")

   if len(i) == 2: #1 byte value
        if n == 0: #Regular
            return (int(i,16))
        elif n == 1: #CPS3
            return (int(i,16))
   elif len(i) == 4: #2 bytes value
        if n == 0: #Regular
            a = int(i[0:2],16)
            b = int(i[2:4],16)
            bin_a = (bin(a)[3:])
            bin_b = (bin(b)[3:])
            bin_val = bin_a + bin_b
            return (int(bin_val,2))
        elif n == 1: #CPS3
            a = int(i[0:2],16)
            b = int(i[2:4],16)
            bin_a = (bin(a)[3:])
            bin_b = (bin(b)[3:])
            bin_val = bin_a + bin_b
            return (int(bin_val,2))
   elif len(i) == 6: #3 bytes value
        if n == 0: #Regular
            a = int(i[0:2],16)
            b = int(i[2:4],16)
            c = int(i[4:6],16)
            bin_a = (bin(a)[3:])
            bin_b = (bin(b)[3:])
            bin_c = (bin(c)[3:])
            bin_val = bin_a + bin_b + bin_c
            return (int(bin_val,2))
        elif n == 1: #CPS3
            a = int(i[0:2],16)
            b = int(i[2:4],16)
            c = int(i[4:6],16)
            bin_a = (bin(a)[3:])
            bin_b = (bin(b)[3:])
            bin_c = (bin(c)[3:])
            bin_val = bin_a + bin_b + bin_c
            return (int(bin_val,2))

def RawConvertor_fromfile(): #Opens file and analyzes first Midi header info.

    try:
        Tempo_Multiplier = float(BPM_multiplier_Entry.get())
    except ValueError:
        messagebox.showerror(title=" (ERROR ID:13)", message="Incorrect Tempo multiplier format! Value must be a number!")
        raise Exception("Incorrect Tempo multiplier format")
    
    global Music_File
    global output_save_file
    #Opening the raw data file, and getting the header info
    root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("midi files","*.mid"), ("all files","*.*")))

    output_save_file = filedialog.asksaveasfilename(initialdir = "Resources", initialfile= "datafile.dat" ,title = "Select where to save your converted file.",filetypes = ((".dat files","*.dat"), ("all files","*.*")))
    try:   
        with MidiFile(root.filename) as Music_File:
            Tempo_set_initial = False
            global Command_C1 
            Command_C1 = "0501"
            for i, track in enumerate(Music_File.tracks):
                for msg in track:
                        if msg.type == "set_tempo":
                            tempo_CPS3 = round(Tempo_Multiplier * tempo2bpm(msg.tempo))
                            if Tempo_set_initial == False:
                                BPM_Entry.config(state="normal")
                                BPM_Entry.delete(0, END)
                                BPM_Entry.insert(END,(round(tempo2bpm(msg.tempo))))
                                BPM_Entry.config(state="readonly")
                                Tempo_set_initial = True
                            Command_C1 = Val_to_var_length(tempo_CPS3,1)
                        if msg.type == "instrument_name":
                            if i == 0:
                                Track_Information_lookup.Track_0_OG_Intrument = str(msg.name)
                            elif i == 1:
                                Track_Information_lookup.Track_1_OG_Intrument = str(msg.name)
                            elif i == 2:
                                Track_Information_lookup.Track_2_OG_Intrument = str(msg.name)
                            elif i == 3:
                                Track_Information_lookup.Track_3_OG_Intrument = str(msg.name)
                            elif i == 4:
                                Track_Information_lookup.Track_4_OG_Intrument = str(msg.name)
                            elif i == 5:
                                Track_Information_lookup.Track_5_OG_Intrument = str(msg.name)
                            elif i == 6:
                                Track_Information_lookup.Track_6_OG_Intrument = str(msg.name)
                            elif i == 7:
                                Track_Information_lookup.Track_7_OG_Intrument = str(msg.name)
                            elif i == 8:
                                Track_Information_lookup.Track_8_OG_Intrument = str(msg.name)
                            elif i == 9:
                                Track_Information_lookup.Track_9_OG_Intrument = str(msg.name)
                            elif i == 10:
                                Track_Information_lookup.Track_10_OG_Intrument = str(msg.name)
                            elif i == 11:
                                Track_Information_lookup.Track_11_OG_Intrument = str(msg.name)
                            elif i == 12:
                                Track_Information_lookup.Track_12_OG_Intrument = str(msg.name)
                            elif i == 13:
                                Track_Information_lookup.Track_13_OG_Intrument = str(msg.name)
                            elif i == 14:
                                Track_Information_lookup.Track_14_OG_Intrument = str(msg.name)
                            elif i == 15:                
                                Track_Information_lookup.Track_15_OG_Intrument = str(msg.name)
                        if msg.type == "track_name":
                            if i == 0:
                                Track_Information_lookup.Track_0_OG_Track_name = str(msg.name)
                            elif i == 1:
                                Track_Information_lookup.Track_1_OG_Track_name = str(msg.name)
                            elif i == 2:
                                Track_Information_lookup.Track_2_OG_Track_name = str(msg.name)
                            elif i == 3:
                                Track_Information_lookup.Track_3_OG_Track_name = str(msg.name)
                            elif i == 4:
                                Track_Information_lookup.Track_4_OG_Track_name = str(msg.name)
                            elif i == 5:
                                Track_Information_lookup.Track_5_OG_Track_name = str(msg.name)
                            elif i == 6:
                                Track_Information_lookup.Track_6_OG_Track_name = str(msg.name)
                            elif i == 7:
                                Track_Information_lookup.Track_7_OG_Track_name = str(msg.name)
                            elif i == 8:
                                Track_Information_lookup.Track_8_OG_Track_name = str(msg.name)
                            elif i == 9:
                                Track_Information_lookup.Track_9_OG_Track_name = str(msg.name)
                            elif i == 10:
                                Track_Information_lookup.Track_10_OG_Track_name = str(msg.name)
                            elif i == 11:
                                Track_Information_lookup.Track_11_OG_Track_name = str(msg.name)
                            elif i == 12:
                                Track_Information_lookup.Track_12_OG_Track_name = str(msg.name)
                            elif i == 13:
                                Track_Information_lookup.Track_13_OG_Track_name = str(msg.name)
                            elif i == 14:
                                Track_Information_lookup.Track_14_OG_Track_name = str(msg.name)
                            elif i == 15:                
                                Track_Information_lookup.Track_15_OG_Track_name = str(msg.name)
            convert_Button = Button(root, text="Convert",bg= Blue_Salvia, fg= Dark_Olive_Slate, command=lambda: ConvertProcess(Music_File))
            convert_Button.place(relx = 0.87, rely = 0.93, anchor = CENTER, width="75")

            Other_entry.config(state="normal")
            Other_entry.delete(0, 'end')
            Other_entry.insert(END,output_save_file)
            Other_entry.config(state="readonly")
    except EOFError:
        messagebox.showerror(title="MIDI Error! (ERROR ID:5.1)", message="mido EOFError, file format may be wrong or corrupted. Aborting conversion...")
        raise Exception("EOFError")    
    except FileNotFoundError:
        messagebox.showinfo(title="Roar?", message="Please select a MIDI file...")
    except OSError:
        messagebox.showerror(title="MIDI Error! (ERROR ID:5.2)", message="mido IOError,  file format may be wrong or corrupted. Aborting conversion...")
        raise Exception("IOError")       


def ConvertProcess (mid): #splitting the track chunk into the individual tracks and analyzing them individually with Track_Converter. (this is connected to the UI button Convert.)
    global output_save_file
    global Delta_data_list
    Data = []
    Delta_data_list = []
    Header_Data = ["000021"] #CPS3 Header
    Track_Offset = 33
    No = 0 #Remove tracks
    Data.append(f"C1{Command_C1}01")
    Pitch_shift = Pitch_shift_slider.get()
    Offset_shift = 0

    try:
        Tempo_Multiplier = float(BPM_multiplier_Entry.get())
    except ValueError:
        messagebox.showerror(title=" (ERROR ID:13)", message="Incorrect Tempo multiplier format! Value must be a number!")
        raise Exception("Incorrect Tempo multiplier format")

    class Delta_Sync :
        Delta_Tot_0 = 0
        Delta_Tot_1 = 0
        Delta_Tot_2 = 0
        Delta_Tot_3 = 0
        Delta_Tot_4 = 0
        Delta_Tot_5 = 0
        Delta_Tot_6 = 0
        Delta_Tot_7 = 0
        Delta_Tot_8 = 0
        Delta_Tot_9 = 0
        Delta_Tot_10 = 0
        Delta_Tot_11 = 0
        Delta_Tot_12 = 0
        Delta_Tot_13 = 0
        Delta_Tot_14 = 0
        Delta_Tot_15 = 0

        D_tot = [Delta_Tot_0,Delta_Tot_1,Delta_Tot_2,Delta_Tot_3,Delta_Tot_4,Delta_Tot_5,Delta_Tot_6,Delta_Tot_7,Delta_Tot_8,Delta_Tot_9,Delta_Tot_10,Delta_Tot_11,Delta_Tot_12,Delta_Tot_13,Delta_Tot_14,Delta_Tot_15]

        Delta_Dif_0 = 0
        Delta_Dif_1 = 0
        Delta_Dif_2 = 0
        Delta_Dif_3 = 0
        Delta_Dif_4 = 0
        Delta_Dif_5 = 0
        Delta_Dif_6 = 0
        Delta_Dif_7 = 0
        Delta_Dif_8 = 0
        Delta_Dif_9 = 0
        Delta_Dif_10 = 0
        Delta_Dif_11 = 0
        Delta_Dif_12 = 0
        Delta_Dif_13 = 0
        Delta_Dif_14 = 0
        Delta_Dif_15 = 0

        D_Dif = [Delta_Dif_0,Delta_Dif_1,Delta_Dif_2,Delta_Dif_3,Delta_Dif_4,Delta_Dif_5,Delta_Dif_6,Delta_Dif_7,Delta_Dif_8,Delta_Dif_9,Delta_Dif_10,Delta_Dif_11,Delta_Dif_12,Delta_Dif_13,Delta_Dif_14,Delta_Dif_15]

    Delta_Highest = 0

    for i, track in enumerate(mid.tracks):

        No = i
        if -1 < No < 16 :

            if i == 0 :
                Track_Volume_increase = (int(Track_0_Volume.get()))
                Command_C4 = (hex(int(Track_0_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_0_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_0_C6_Value.get())))[2:].zfill(2)
            elif i == 1 :
                Track_Volume_increase = (int(Track_1_Volume.get()))
                Command_C4 = (hex(int(Track_1_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_1_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_1_C6_Value.get())))[2:].zfill(2)
            elif i == 2 :
                Track_Volume_increase = (int(Track_2_Volume.get()))
                Command_C4 = (hex(int(Track_2_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_2_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_2_C6_Value.get())))[2:].zfill(2)
            elif i == 3 :
                Track_Volume_increase = (int(Track_3_Volume.get()))
                Command_C4 = (hex(int(Track_3_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_3_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_3_C6_Value.get())))[2:].zfill(2)
            elif i == 4 :
                Track_Volume_increase = (int(Track_4_Volume.get()))
                Command_C4 = (hex(int(Track_4_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_4_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_4_C6_Value.get())))[2:].zfill(2)
            elif i == 5 :
                Track_Volume_increase = (int(Track_5_Volume.get()))
                Command_C4 = (hex(int(Track_5_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_5_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_5_C6_Value.get())))[2:].zfill(2)
            elif i == 6 :
                Track_Volume_increase = (int(Track_6_Volume.get()))
                Command_C4 = (hex(int(Track_6_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_6_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_6_C6_Value.get())))[2:].zfill(2)
            elif i == 7 :
                Track_Volume_increase = (int(Track_7_Volume.get()))
                Command_C4 = (hex(int(Track_7_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_7_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_7_C6_Value.get())))[2:].zfill(2)
            elif i == 8 :
                Track_Volume_increase = (int(Track_8_Volume.get()))
                Command_C4 = (hex(int(Track_8_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_8_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_8_C6_Value.get())))[2:].zfill(2)
            elif i == 9 :
                Track_Volume_increase = (int(Track_9_Volume.get()))
                Command_C4 = (hex(int(Track_9_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_9_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_9_C6_Value.get())))[2:].zfill(2)
            elif i == 10 :
                Track_Volume_increase = (int(Track_10_Volume.get()))
                Command_C4 = (hex(int(Track_10_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_10_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_10_C6_Value.get())))[2:].zfill(2)
            elif i == 11 :
                Track_Volume_increase = (int(Track_11_Volume.get()))
                Command_C4 = (hex(int(Track_11_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_11_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_11_C6_Value.get())))[2:].zfill(2)
            elif i == 12 :
                Track_Volume_increase = (int(Track_12_Volume.get()))
                Command_C4 = (hex(int(Track_12_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_12_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_12_C6_Value.get())))[2:].zfill(2)
            elif i == 13 :
                Track_Volume_increase = (int(Track_13_Volume.get()))
                Command_C4 = (hex(int(Track_13_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_13_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_13_C6_Value.get())))[2:].zfill(2)
            elif i == 14 :
                Track_Volume_increase = (int(Track_14_Volume.get()))
                Command_C4 = (hex(int(Track_14_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_14_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_14_C6_Value.get())))[2:].zfill(2)
            elif i == 15 :
                Track_Volume_increase = (int(Track_15_Volume.get()))
                Command_C4 = (hex(int(Track_15_Instrument.get())))[2:].zfill(2)
                Command_C7 = (hex(int(Track_15_Pan.get())))[2:].zfill(2)
                Command_C6 = (hex(int(Track_15_C6_Value.get())))[2:].zfill(2)
            else:
                messagebox.showerror(title="More than 16 tracks detected! (ERROR ID:6)", message="This MIDI contains more than 16 tracks (CPS3 MAX), aborting conversion...")
                raise Exception("16+ track MIDI detected! Aborting conversion...")   
            Data.append("C20001") #C2 Command.)  
            Data.append(f"C4{Command_C4}01") #C4 COMMAND
            Data.append(f"C50001") #C5 COMMAND (unkn)
            Data.append(f"C6{Command_C6}01") #C6 COMMAND
            Data.append(f"C7{Command_C7}01") #C7 COMMAND
            Data.append(f"C83700D0") #C8 COMMAND (unkn)


            volume_increase = 60 + Track_Volume_increase
            Pitch_Change = Pitch_shift #TO-DO
            Hold_increase = 0 #TO-DO
            Delta_time = 0
            Previous_hold = 0
            Note_pressed = False #note on active
            Command_Active = False #Command position

            Delta_Total = 0
            Delta_Total_check = 0
            def constants():
                constants.Percussion_Boolean = 0
            Volume_warning = False
            constants()

            def Drumkit_maker(Instrument_list):
                for i in range (27,87):
                    if int(msg.note+Pitch_Change) == i :
                        if constants.Percussion_Boolean != i:
                            Data.append(f"C4{Instrument_list[i-27][0]}") #Hat open
                            print(Instrument_list[i-27])
                            constants.Percussion_Boolean = 0 #Hat open            


            for msg in track:
                if msg.type == "note_on":
                    if (str(hex(msg.velocity)))[2:].zfill(2) == "00": #NOTE OFF (but note-on type)
                        if Note_pressed == False :
                            print (msg)
                            messagebox.showerror(title="Incorrect MIDI type! (ERROR ID:7)", message="Non-Monophonic Midi detected! Aborting conversion...")
                            raise Exception("Non-Monophonic Midi detected! Aborting conversion...")
                        Delta_time = Delta_time + (msg.time)
                        Data.append (Val_to_var_length (Delta_time+Hold_increase,0)) #Hold
                        Previous_hold = Delta_time+Hold_increase #Hold Get
                        Note_pressed = False
                        Delta_time = 0
                        Command_Active = False
                    else: #NOTE ON
                        if Note_pressed == True :
                            print (msg)
                            messagebox.showerror(title="Incorrect MIDI type! (ERROR ID:8)", message="Non-Monophonic Midi detected! Aborting conversion...")
                            raise Exception("Non-Monophonic Midi detected! Aborting conversion...")
                        Delta_time = Delta_time + (msg.time)
                        if (msg.velocity+volume_increase) < 128 : #Volume
                            messagebox.showerror(title="Volume too low! (ERROR ID:9)", message="Volume in track {} is lower than 0x80! Aborting conversion...".format(i)) #Volume
                            raise Exception("Volume in track {} is lower than 0x80! Aborting conversion...".format(i)) #Volume
                        elif (msg.velocity+volume_increase) > 191  : #Volume
                            if Volume_warning == False:
                                Volume_warning = True
                                messagebox.showwarning(title="Volume too high!", message="Volume in track {} is higher than 0xC0! Lowering volume...".format(i)) #Volume
                            msg.velocity = msg.velocity + (191 - (msg.velocity+volume_increase))
   
                        Data.append(Val_to_var_length (Previous_hold+Delta_time+Hold_increase,1)) #Release / Delta
                        Delta_Total_check = Delta_Total_check + Previous_hold+Delta_time+Hold_increase
                        if Command_C4 == "00": #PERCUSSION INSTRUMENT SPLIT
                            Drumkit_maker(Drumkit_Default)
                        Data.append((str(hex(msg.velocity+volume_increase)))[2:].zfill(2)) #Volume       
                        
                        Data.append((str(hex(msg.note+Pitch_Change)))[2:].zfill(2)) #Pitch
                        if (msg.note+Pitch_Change) > 128 :  #Pitch
                            messagebox.showerror(title="Note pitch too high! (ERROR ID:10)", message="Pitch is higher than 0x80! Aborting conversion...") #Pitch
                            raise Exception("Pitch is higher than 0x80! Aborting conversion...") #Pitch

                        Delta_time = 0
                        Note_pressed = True
                        Command_Active = False
                elif msg.type == "note_off": #NOTE OFF
                    if Note_pressed == False :
                            print (msg)
                            messagebox.showerror(title="Incorrect MIDI type! (ERROR ID:11)", message="Non-Monophonic Midi detected! Aborting conversion...")
                            raise Exception("Non-Monophonic Midi detected! Aborting conversion...")
                    Delta_time = Delta_time + (msg.time)  
                    Data.append (Val_to_var_length (Delta_time+Hold_increase,0)) #Hold
                    Previous_hold = Delta_time+Hold_increase #Hold Get
                    Note_pressed = False
                    Delta_time = 0
                    Command_Active = False
                elif msg.type == "set_tempo":
                    if Note_pressed == True :
                        messagebox.showerror(title="'Set_tempo' message error! (ERROR ID:12)", message="Tempo change detected while 'Note-On'! Aborting conversion...")
                        raise Exception("Tempo change detected while 'Note-On'! Aborting conversion...")
                    else:
                        Delta_time = Delta_time + (msg.time)
                        Data.append(Val_to_var_length (Previous_hold+Delta_time+Hold_increase,1)) #Release / Delta
                        Delta_Total_check = Delta_Total_check + Previous_hold+Delta_time+Hold_increase
                        cps3_tempo = round(
                           Tempo_Multiplier * tempo2bpm(msg.tempo))
                        cps3_tempo = Val_to_var_length (cps3_tempo,1)
                        Delta_time = 0
                        Data.append(f"C1{cps3_tempo}")
                elif msg.type == "end_of_track":
                    if Note_pressed == False :
                        Data.append(Val_to_var_length (Previous_hold+Delta_time+Hold_increase,1)) #Release / Delta
                        Delta_Total = Delta_Total + Previous_hold+Delta_time+Hold_increase
                        Delta_Total_check = Delta_Total_check + Previous_hold+Delta_time+Hold_increase
                    else:
                        messagebox.showerror(title="Midi error!", message="Midi track ends before all notes are off, aborting conversion...")
                        raise Exception ("Track ends with no note off") 
                else:
                    Delta_time = Delta_time + (msg.time)

                Delta_Total = Delta_Total + msg.time

                Delta_Total = Delta_Total_check #REMOVE IF YOU WISH TO SEE THE REAL MIDI DELTA

            print (f"Delta T{i} Total: {Delta_Total}")
            print (f"Delta Total Check: {Delta_Total_check}")    

            
            i_varlength = Val_to_var_length(i,0)   #gets id in byte form
            Data.append(f"ABCDEF{i_varlength}FAFBFC") #creates a placeholder for the loop end

            Delta_Sync.D_tot[i] = Delta_Total #calculates the difference between deltas of all tracks
            if Delta_Highest < Delta_Total:
                Delta_Highest = Delta_Total    

            #after this line all data is counted for the next track offset.
            String_Data = List_Useless_remover(Data,4)
            Header_Data.append((hex(round((int(len(String_Data)))/2+Track_Offset)))[2:].zfill(4))#Counts the offset.
        else:
            messagebox.showerror(title="Midi error! (ERROR ID:14)", message="current MIDI has more than 16 tracks! Aborting conversion...")
            raise Exception ("16+ tracks MIDI detected.")     

    print (Delta_Sync.D_tot)
    Final_Data = (List_Useless_remover(Data,3))

    out_of_range = False
    for num_range in range(0,16): #makes a new note so that all songs end at the same delta.
        Delta_Sync.D_Dif[num_range] = Delta_Highest - Delta_Sync.D_tot[num_range]
        if out_of_range == False:
            print (f"Track {num_range} Delta Difference: {Delta_Sync.D_Dif[num_range]}")
            print (Val_to_var_length(Delta_Sync.D_Dif[num_range]+3,1))
        Var_num_range = Val_to_var_length(num_range,0)
        Var_dif_delta = Val_to_var_length(Delta_Sync.D_Dif[num_range]+3,1)

        sync_delta_note = f"81408100{Var_dif_delta}D400FF"
        try:
            if len(Var_dif_delta) == 2:
                Offset_shift = Offset_shift + 0
                Header_Data[num_range+1] = hex(int(Header_Data[num_range+1],16)+Offset_shift)[2:].zfill(4)
                sync_delta_note = f"814003{Var_dif_delta}D400FF"
            elif len(Var_dif_delta) == 4:
                Offset_shift = Offset_shift + 2
                Header_Data[num_range+1] = hex(int(Header_Data[num_range+1],16)+Offset_shift)[2:].zfill(4)
            elif len(Var_dif_delta) == 6:
                Offset_shift = Offset_shift + 3
                Header_Data[num_range+1] = hex(int(Header_Data[num_range+1],16)+Offset_shift)[2:].zfill(4)
        except:
            print("Out of range index")
            out_of_range = True
        
        if out_of_range == False:
            print (f"{sync_delta_note}\n")

            Final_Data = Final_Data.replace(
                f"ABCDEF{Var_num_range}FAFBFC", sync_delta_note
            )
    
    Header_Data = Header_Data[:-1]
    Header_Data = (List_Useless_remover(Header_Data,4))
    Header_Data = Header_Data.ljust(66,"0")

    try:
        output = open("Resources//log.txt", "r+")
        output.truncate(0)
        output_file2 = open(output_save_file, "wb+")
        output_file2.truncate(0)
    except FileNotFoundError:
        messagebox.showerror(title="File not found! (ERROR ID:17)", message="Directory or file not found, if this is unexpected please restart the application. ")
    print (Header_Data, file= output)
    print (Final_Data, file= output)
    print ("\nDELTA TIMES:\n", file= output)
    print (Delta_data_list, file= output)
    Header_out = binascii.unhexlify((str(Header_Data)).replace(" ","").replace("\n",""))
    Sequence_out = binascii.unhexlify((str(Final_Data)).replace(" ","").replace("\n",""))

    output_file2.write(Header_out)
    output_file2.write(Sequence_out)
    output.close()
    output_file2.close()
    TK_Message("Conversion Complete!\n\n(Check 'log.txt' for more info)","Roar!")



def TK_Message(input,Title): #SHORTCUT FOR MAKING MESSAGE BOXES
    messagebox.showinfo(title=Title, message=input)


def Poly_2_Mono_Window(): #POLY TO MONO WINDOW

    def Poly_2_Mono_converter(polymidi):
        NEW_Mid = MidiFile()
        Note_on_as_note_off = False
        for i, track in enumerate(polymidi.tracks):

            Track_new = MidiTrack()
            print('Track {}: {}'.format(i, track.name))
            Previous_note = 0
            Previous_velocity = 0
            Previous_channel = 0
            Previous_message_Delta = 0
            Extra_delta_add = 0

            poly_2_mono_total_delta_original = 0
            poly_2_mono_total_delta_converted = 0

            #if Default_tempo == False:
                #Track_new.append(MetaMessage("set_tempo", tempo = 500000))
                #Default_tempo = True

            Note_on_pressed = False
            Note_off_pressed = False

            last_false = ""

            in_between_commands = []

            for msg in track:

                poly_2_mono_total_delta_original = poly_2_mono_total_delta_original + msg.time

                if msg.type == "note_on": 
                    #print (msg.type)
                    if msg.velocity != 0:
                        #NOTE ON
                        if Note_off_pressed == True:
                            #First Note (not the first ever)
                            if Note_on_pressed == False:

                                if Note_on_as_note_off == True: #Pastes note off
                                    Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=0, time=Previous_message_Delta))
                                else:
                                    Track_new.append(Message("note_off", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=Previous_message_Delta))
                                Track_new.extend(in_between_commands)
                                in_between_commands = []
                                #grabs note on data
                                Previous_note = msg.note
                                Previous_velocity = msg.velocity
                                Previous_channel = msg.channel
                                Previous_message_Delta = msg.time + Extra_delta_add

                                Extra_delta_add = 0  

                                Note_on_pressed = True
                                Note_off_pressed = False
                                last_false = "note_off"

                            else: #Note on while note on already pressed
                                if msg.time+Extra_delta_add != 0:
                                    Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=Previous_message_Delta))
                                    Track_new.extend(in_between_commands)
                                    if Note_on_as_note_off == True:
                                        Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=0, time=msg.time))
                                    else:
                                        Track_new.append(Message("note_off", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=msg.time))
                                    in_between_commands = []
                                    Previous_note = msg.note
                                    Previous_velocity = msg.velocity
                                    Previous_channel = msg.channel
                                    Previous_message_Delta = 0


                                    last_false = "note_off"
                                else: 
                                    #multi note
                                    if msg.note > Previous_note:
                                        #higher pitched note in multi note
                                        Previous_note = msg.note

                                        last_false = "note_off"         


                            Note_on_pressed = True
                            Note_off_pressed = False

                            last_false = "note_off"
                        else:
                            #Followup
                            if Note_on_pressed == True:
                                if msg.time == 0:
                                    #multi note
                                    if msg.note > Previous_note:
                                        #higher pitched note in multi note
                                        Previous_note = msg.note

                                        last_false = "note_off"
                                else:
                                    #non-instant note after note on.
                                    Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=Previous_message_Delta))
                                    Track_new.extend(in_between_commands)
                                    if Note_on_as_note_off == True:
                                        Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=0, time=msg.time+Extra_delta_add))
                                    else:
                                        Track_new.append(Message("note_off", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=msg.time+Extra_delta_add))
                                    in_between_commands = []
                                    Previous_note = msg.note
                                    Previous_velocity = msg.velocity
                                    Previous_channel = msg.channel
                                    Previous_message_Delta = 0

                                    Extra_delta_add = 0

                                    Note_on_pressed = True
                                    last_false = "note_off"       
                            else:  
                                #First ever note on
                                Previous_note = msg.note
                                Previous_velocity = msg.velocity
                                Previous_channel = msg.channel
                                Previous_message_Delta = msg.time

                                Note_on_pressed = True        
                    else:
                        Note_on_as_note_off = True
                        #NOTE OFF
                        if msg.note == Previous_note:
                            #Note off right note
                            if Note_on_pressed == True:
                                Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=Previous_message_Delta))
                                Track_new.extend(in_between_commands)
                                in_between_commands = []

                                Previous_message_Delta = msg.time + Extra_delta_add
                                Extra_delta_add = 0

                                Note_off_pressed = True
                                Note_on_pressed = False
                            else:
                                Previous_message_Delta = Previous_message_Delta + msg.time
                            last_false = "note_on"

                        else:
                            #note off wrong note
                            if msg.time != 0:
                                #wrong note off with delta
                                Extra_delta_add = msg.time + Extra_delta_add

                            last_false = "note_on"                                

                elif msg.type == "note_off":
                    #print (msg.type)
                    #NOTE OFF
                    if msg.note == Previous_note:
                        #Note off right note
                        if Note_on_pressed == True:
                            Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=Previous_message_Delta))
                            Track_new.extend(in_between_commands)
                            in_between_commands = []

                            Previous_message_Delta = msg.time + Extra_delta_add
                            Extra_delta_add = 0

                            Note_off_pressed = True
                            Note_on_pressed = False

                        else:
                            Previous_message_Delta = msg.time + Extra_delta_add + Previous_message_Delta
                            Extra_delta_add = 0

                        last_false = "note_on"

                    else:
                        #note off wrong note
                        if msg.time != 0:
                            #wrong note off with delta
                            Extra_delta_add = msg.time + Extra_delta_add

                        last_false = "note_on"

                elif msg.type == "end_of_track":
                    #print (msg.type)
                    if Note_on_pressed == True: #Note on pressed
                        Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=Previous_message_Delta))
                        Track_new.extend(in_between_commands)
                        if Note_on_as_note_off == True:
                            Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=0, time=Previous_message_Delta))
                        else:
                            Track_new.append(Message("note_off", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=Previous_message_Delta))
                        in_between_commands = []


                        Track_new.append(msg)
                    elif Note_off_pressed == True: #note off pressed
                        if Note_on_as_note_off == True:
                            Track_new.append(Message("note_on", channel=Previous_channel, note=Previous_note, velocity=0, time=Previous_message_Delta))
                        else:
                            Track_new.append(Message("note_off", channel=Previous_channel, note=Previous_note, velocity=Previous_velocity, time=Previous_message_Delta+Extra_delta_add))
                        Track_new.extend(in_between_commands)
                        in_between_commands = []
                        

                        Track_new.append(msg)        
                else: #other commands
                    if Note_on_pressed == True: #Note on pressed
                        in_between_commands.append(msg)
                    elif Note_off_pressed == True: #Note off pressed
                        in_between_commands.append(msg)
                    else:
                        Track_new.append(msg)              
            
            NEW_Mid.tracks.append(Track_new)

            for msg_edit in Track_new:
                poly_2_mono_total_delta_converted = poly_2_mono_total_delta_converted + msg_edit.time

            print(f"Track's Original delta time: {poly_2_mono_total_delta_original}")

            print(f"Track's Converted delta time: {poly_2_mono_total_delta_converted}")

            if poly_2_mono_total_delta_original == poly_2_mono_total_delta_converted:
                print ('\033[92m'+"NO DELTA DESYNC FOUND"+'\033[0m')
            else:
                print ('\033[91m'+"ERROR: DELTA TIMES DO NOT MATCH!"+'\033[0m')     

        save_file = filedialog.asksaveasfilename(initialdir = "/",title = "Select where to save your file.",defaultextension="*.mid" ,filetypes = (("midi files","*.mid"), ("all files","*.*")))
        NEW_Mid.save(f"{save_file}")
        global saved_file_name
        saved_file_name = (f"{save_file}")
        TK_Message("Completed!\n\n(Results may still be unexpected)","")
    
    try:
        root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("midi files","*.mid"), ("all files","*.*")))  
        with MidiFile(root.filename) as Music_File:
            Poly_2_Mono_converter(Music_File)
            print(f"SAVED OUTPUT: {saved_file_name}")
        with open(f"{root.filename}", "rb") as poly_midi_file_opened:
            poly_data_time_div = poly_midi_file_opened.read()
            poly_data_time_div = poly_data_time_div[12:14]
            print (poly_data_time_div)            
            poly_midi_file_opened.close()
        with open(f"{saved_file_name}", "r+b") as mono_midi_file_opened:
            mono_midi_file_opened.seek(12)
            mono_midi_file_opened.write(poly_data_time_div)
            mono_midi_file_opened.close()    
    except IndexError:
        messagebox.showerror(title="IndexError! (ERROR ID:16)", message="This MIDI is either in an incorrect format, or in a format not supported by this tool.")


 
def Midi_Analyzer():
    
    buut = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("midi files","*.mid"), ("all files","*.*")))

    stdout = open("Analyzer_Output.txt", 'w+')


    mid = MidiFile(buut)

    for i, track in enumerate(mid.tracks):
        Total_delta_analysis = 0
        print('Track {}: {}'.format(i, track.name), file = stdout )
        for msg in track:
            print(msg, file = stdout )
            Total_delta_analysis = Total_delta_analysis + msg.time
            print((f"Current total Delta: {Total_delta_analysis}"), file = stdout )

#VISUAL STUFF (buttons, entries, sliders etc.)

#Toolbar

toolbar = Frame(root)
toolbar.pack(side=TOP, fill=X)
toolbar.config(background=Blue_Salvia)

b1 = Button(toolbar, text="Load",borderwidth= 0,width=7,bg= Blue_Salvia, fg= Dark_Olive_Slate, command= RawConvertor_fromfile)
b1.pack(side=LEFT, padx=0, pady=0) #Load file

b2_message = "Q: Which file format is currently supported?\nA: At the moment only .mid files.\n\nQ: I've got an error saying something about 'monophonic midis', what does it mean?\nA: 'Monophonic MIDIs' are a type of midi that essentially don't play 2 notes at the same time in the same track, CPS3 tracks use that form of sequence data.\n TL;DR: just use Poly 2 Mono.\n\nQ:I've converted the midi and got a bunch of hex data, what do I do?\nA:The program outputs in the form of CPS3 raw music data, meaning that such data still needs to be pasted into file 10 and encrypted back. I chose to make it this way so that people don't accidentally mess up their own roms while using the tool\n\nQ: Where do I need to save the 'Datafile.dat' file?\nA: inside your fba folder there should be a folder called 'research', simply drop it in there."
b2 = Button(toolbar, text="Help",borderwidth= 0,width=7,bg= Blue_Salvia, fg= Dark_Olive_Slate, command=lambda: TK_Message(b2_message,"Common questions & answers."))
b2.pack(side=LEFT, padx=0, pady=0) #Help, QnA

b3 = Button(toolbar, text="Poly to Mono",borderwidth= 0,width=12,bg= Blue_Salvia, fg= Dark_Olive_Slate, command=lambda: Poly_2_Mono_Window())
b3.pack(side=LEFT, padx=0, pady=0) #opens Poly to mono converter

b4_message = "TigerS - Midi raw to CPS3 music convertor - Made by Babro.\n\nCredits to DrewDos for making the original CPS3 sfx documentation (not to mention the CPS3 spritemodding tool.) and helping me understand how the sound samples work.\n\nCredits to Insertusernamehere, creator of the CPS3 to MIDI tool who provided a lot of useful information, including how sequence data works, location of the various music data, and sharing the source code of his program.\nCredits to 'Mido' for existing.\n\nCredits to 'The Sonic Spot' for providing all the information about the MIDI file format (and the Wayback Machine for allowing me to see their old website).\n\nCredits to the Third Strike, 4rd Strike, HFTF, and Red Earth communities for helping me gather info.\n\nCredits to Visual Studio Code for crashing every 5 minutes."
b4 = Button(toolbar, text="Credits",borderwidth= 0,width=7,bg= Blue_Salvia, fg= Dark_Olive_Slate, command=lambda: TK_Message(b4_message,"Credits"))
b4.pack(side=LEFT, padx=0, pady=0) #Credits

b5 = Button(toolbar, text="Save ID layout",borderwidth= 0,width=12,bg= Blue_Salvia, fg= Dark_Olive_Slate, command=lambda: Save_instrument_layout())
b5.pack(side=LEFT, padx=0, pady=0) #Save Instrument Layout

b6  = Button(toolbar, text="Load ID layout",borderwidth= 0,width=12,bg= Blue_Salvia, fg= Dark_Olive_Slate, command=lambda: Load_instrument_layout())
b6.pack(side=LEFT, padx=0, pady=0) #Open Instrument Layout

b7 = Button(toolbar, text="Analyze MIDI",borderwidth= 0,width=12,bg= Blue_Salvia, fg= Dark_Olive_Slate, command=lambda: Midi_Analyzer())
b7.pack(side=LEFT, padx=0, pady=0) #Open Instrument Layout

#ComboBox
#InstrumentRange = range(1 , 60)
#InstrumentList = []
#for n in InstrumentRange:
#    InstrumentList.append(n)
#InstrumentSelectBox = ttk.Combobox(root, values=InstrumentList, background= Blue_Salvia, foreground=Dark_Olive_Slate )
#InstrumentSelectBox.insert (END,"18")
#InstrumentSelectBox.place(relx = 0.55, rely = 0.65, anchor = CENTER, width=40)

#Track editor window
for i in range(0,16):
    y = 0.042 * i

    globals()[f"Track_{i}_ID"] = i

    globals()[f"Track_{i}_Volume"] = Entry(root, font=(Font_UI, 8, BOLD),justify='center', bg = Blue_Salvia, borderwidth=2, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
    globals()[f"Track_{i}_Volume"].place(relx = 0.23, rely = (0.31 + y), anchor = CENTER, width=30)
    globals()[f"Track_{i}_Volume"].insert(END,0)
    globals()[f"Track_{i}_Volume"].config(state="readonly")

    globals()[f"Track_{i}_Pan"] = Entry(root, font=(Font_UI, 8, BOLD),justify='center', bg = Blue_Salvia, borderwidth=2, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
    globals()[f"Track_{i}_Pan"].place(relx = 0.34, rely = (0.31 + y), anchor = CENTER, width=30)
    globals()[f"Track_{i}_Pan"].insert(END,64)
    globals()[f"Track_{i}_Pan"].config(state="readonly")

    globals()[f"Track_{i}_Instrument"] = Entry(root, font=(Font_UI, 8, BOLD),justify='center', bg = Blue_Salvia, borderwidth=2, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
    globals()[f"Track_{i}_Instrument"].place(relx = 0.45, rely = (0.31 + y), anchor = CENTER, width=30)
    globals()[f"Track_{i}_Instrument"].insert(END,23)
    globals()[f"Track_{i}_Instrument"].config(state="readonly")

    globals()[f"Track_{i}_C6_Value"] = Entry(root, font=(Font_UI, 8, BOLD),justify='center', bg = Blue_Salvia, borderwidth=2, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
    globals()[f"Track_{i}_C6_Value"].place(relx = 0.56, rely = (0.31 + y), anchor = CENTER, width=30)
    globals()[f"Track_{i}_C6_Value"].insert(END,78)
    globals()[f"Track_{i}_C6_Value"].config(state="readonly")

Track_Volume_List = [
    Track_0_Volume,Track_1_Volume,Track_2_Volume,Track_3_Volume,Track_4_Volume,Track_5_Volume,Track_6_Volume,Track_7_Volume,Track_8_Volume,Track_9_Volume,Track_10_Volume,Track_11_Volume,Track_12_Volume,Track_13_Volume,Track_14_Volume,Track_15_Volume]
Track_Pan_List = [
    Track_0_Pan,Track_1_Pan,Track_2_Pan,Track_3_Pan,Track_4_Pan,Track_5_Pan,Track_6_Pan,Track_7_Pan,Track_8_Pan,Track_9_Pan,Track_10_Pan,Track_11_Pan,Track_12_Pan,Track_13_Pan,Track_14_Pan,Track_15_Pan]
Track_Instrument_List = [
    Track_0_Instrument,Track_1_Instrument,Track_2_Instrument,Track_3_Instrument,Track_4_Instrument,Track_5_Instrument,Track_6_Instrument,Track_7_Instrument,Track_8_Instrument,Track_9_Instrument,Track_10_Instrument,Track_11_Instrument,Track_12_Instrument,Track_13_Instrument,Track_14_Instrument,Track_15_Instrument]
Track_C6_Value_List = [
    Track_0_C6_Value,Track_1_C6_Value,Track_2_C6_Value,Track_3_C6_Value,Track_4_C6_Value,Track_5_C6_Value,Track_6_C6_Value,Track_7_C6_Value,Track_8_C6_Value,Track_9_C6_Value,Track_10_C6_Value,Track_11_C6_Value,Track_12_C6_Value,Track_13_C6_Value,Track_14_C6_Value,Track_15_C6_Value]

def Volume_Equalizer_all_tracks(Entry):
    try:
        Error_status = False
        Value = int(Entry.get())
        for Track_volume in Track_Volume_List:
            initial_value = int(Track_volume.get())
            if (initial_value + Value) < 1:
                Error_status = True
            else:    
                Track_volume.config(state="normal")
                Track_volume.delete(0, END)
                Track_volume.insert(END,(initial_value + Value))
                Track_volume.config(state="readonly")
        for Track_C6 in Track_C6_Value_List:
            initial_value = int(Track_C6.get())
            if (initial_value - Value) < 1:
                Error_status = True
            else:
                Track_C6.config(state="normal")
                Track_C6.delete(0, END)
                Track_C6.insert(END,(initial_value - Value))
                Track_C6.config(state="readonly")
        if Error_status == True:
            messagebox.showerror(title="Negative Volume values (EQ)! (ERROR ID:18)", message="No negative Volume values allowed, some tracks were left unchanged.")
    except ValueError:
        messagebox.showerror(title="Non-integer value detected! (EQ) (ERROR ID:20)", message="Please refrain from using anything but numbers.")        


def Volume_Amplifier_all_tracks(Entry):
    try:
        Error_status = False
        Value = int(Entry.get())
        for Track_volume in Track_Volume_List:
            initial_value = int(Track_volume.get())
            if (initial_value + Value) < 1:
                Error_status = True
            else:
                Track_volume.config(state="normal")
                Track_volume.delete(0, END)
                Track_volume.insert(END,(initial_value + Value))
                Track_volume.config(state="readonly")
        if Error_status == True:
            messagebox.showerror(title="Negative Volume values (AMP)! (ERROR ID:19)", message="No negative Volume values allowed, some tracks were left unchanged.")
    except ValueError:
        messagebox.showerror(title="Non-integer value detected! (AMP) (ERROR ID:21)", message="Please refrain from using anything but numbers.")      


def openNew_volume_Window():

    newWindow_Volume = Toplevel(root)
    newWindow_Volume.title("VolEdit")
    newWindow_Volume.geometry("230x250")
    newWindow_Volume.config(background= Dark_Olive_Slate) #window config
    newWindow_Volume.resizable(0, 0) #can't resize window
    newWindow_Volume.iconbitmap(default='Resources//546967657253.Babro') #importing images

    Equalizer_volume = Label(newWindow_Volume, text="Equalizer:",bg= Dark_Olive_Slate, fg= Yellow_Sulphur)
    Equalizer_volume.config(font=(Font_UI, 10, BOLD))
    Equalizer_volume.place(relx = 0.5, rely = 0.15, anchor = CENTER)
    

    Equalizer_volume_Entry = Entry(newWindow_Volume, state="normal",font=(Font_UI, 13, BOLD),justify='center',bg = Blue_Salvia, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
    Equalizer_volume_Entry.insert(END, "0")
    Equalizer_volume_Entry.place(relx = 0.20, rely = 0.35, anchor = CENTER, width=60, height=35)

    Equalizer_volume_Button = Button(newWindow_Volume, text="Apply EQ",font=(Font_UI, 9, BOLD),bg= Blue_Salvia, fg= Dark_Olive_Slate)
    Equalizer_volume_Button.config(command= lambda: Volume_Equalizer_all_tracks(Equalizer_volume_Entry))
    Equalizer_volume_Button.place(relx = 0.70, rely = 0.35, anchor = CENTER, height="35", width="90")


    Amplifier_volume = Label(newWindow_Volume, text="Amplifier:",bg= Dark_Olive_Slate, fg= Yellow_Sulphur)
    Amplifier_volume.config(font=(Font_UI, 10, BOLD))
    Amplifier_volume.place(relx = 0.5, rely = 0.55, anchor = CENTER)

    Amplifier_volume_Entry = Entry(newWindow_Volume, state="normal",font=(Font_UI, 13, BOLD),justify='center',bg = Blue_Salvia, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
    Amplifier_volume_Entry.insert(END, "0")
    Amplifier_volume_Entry.place(relx = 0.20, rely = 0.75, anchor = CENTER, width=60, height=35)

    Amplifier_volume_Button = Button(newWindow_Volume, text="Apply AMP",font=(Font_UI, 9, BOLD),bg= Blue_Salvia, fg= Dark_Olive_Slate)
    Amplifier_volume_Button.config(command= lambda: Volume_Amplifier_all_tracks(Amplifier_volume_Entry))
    Amplifier_volume_Button.place(relx = 0.70, rely = 0.75, anchor = CENTER, height="35", width="90")



    Warning = Label(newWindow_Volume, text="DO NOT USE EQUALIZER IF NOT SURE OF WHAT IT DOES",bg= Dark_Olive_Slate, fg= "#606474")
    Warning.config(font=(Font_UI, 6, BOLD))
    Warning.place(relx = 0.5, rely = 0.95, anchor = CENTER)              


def openNewWindow(id,Title,Instrument):

    newWindow = Toplevel(root)
    newWindow.title("Track {} editor.".format(id))
    newWindow.geometry("500x550")
    newWindow.config(background= Dark_Olive_Slate) #window config
    newWindow.resizable(0, 0) #can't resize window
    newWindow.iconbitmap(default='Resources//546967657253.Babro') #importing images

    Volume_message = Label(newWindow, text=("Track {} note volume increase:".format(id)),bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
    Volume_message.config(font=(Font_UI, 10, BOLD))
    Volume_message.place(relx = 0.5, rely = 0.20, anchor = CENTER)


    Track_Volume_SLIDER = Scale(newWindow, from_= -50, to=150)
    Track_Volume_SLIDER.set((Track_Volume_List[id]).get())
    Track_Volume_SLIDER.config(bg = Blue_Salvia, fg = Dark_Olive_Slate, borderwidth= (2), tickinterval=10, length =450, activebackground= Blue_Salvia, highlightbackground=Yellow_Sulphur, troughcolor= Yellow_Sulphur, orient=HORIZONTAL)
    Track_Volume_SLIDER.place(relx = 0.5, rely = 0.30, anchor = CENTER)

    Panning_message = Label(newWindow, text=("Track {} audio panning:".format(id)),bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
    Panning_message.config(font=(Font_UI, 10, BOLD))
    Panning_message.place(relx = 0.5, rely = 0.40, anchor = CENTER)

    Track_Panning_SLIDER = Scale(newWindow, from_= 0, to=127)
    Track_Panning_SLIDER.set((Track_Pan_List[id]).get())
    Track_Panning_SLIDER.config(bg = Blue_Salvia, fg = Dark_Olive_Slate, borderwidth= (2), tickinterval=8, length =450, activebackground= Blue_Salvia, highlightbackground=Yellow_Sulphur, troughcolor= Yellow_Sulphur, orient=HORIZONTAL)
    Track_Panning_SLIDER.place(relx = 0.5, rely = 0.50, anchor = CENTER)

    Instrument_message = Label(newWindow, text=("Track {} instrument:".format(id)),bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
    Instrument_message.config(font=(Font_UI, 10, BOLD))
    Instrument_message.place(relx = 0.20, rely = 0.65, anchor = CENTER)

    InstrumentSelectBox = ttk.Combobox(newWindow, values=Intrument_Groups.ID_instrument_items, background= Blue_Salvia, foreground=Dark_Olive_Slate )
    InstrumentSelectBox.insert (END,(list(Intrument_Groups.ID_instrument_List)[int((Track_Instrument_List[id]).get())]))
    print(int((Track_Instrument_List[id]).get()))
    print((list(Intrument_Groups.ID_instrument_List)[int((Track_Instrument_List[id]).get())]))
    InstrumentSelectBox.place(relx = 0.20, rely = 0.75, anchor = CENTER, width=150)

    Track_C6_Volume_message = Label(newWindow, text=("Track {} Volume:".format(id)),bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
    Track_C6_Volume_message.config(font=(Font_UI, 10, BOLD))
    Track_C6_Volume_message.place(relx = 0.70, rely = 0.65, anchor = CENTER)

    Track_C6_Volume_SLIDER = Scale(newWindow, from_= 0, to=127)
    Track_C6_Volume_SLIDER.set((Track_C6_Value_List[id]).get())
    Track_C6_Volume_SLIDER.config(bg = Blue_Salvia, fg = Dark_Olive_Slate, borderwidth= (2), tickinterval=15, length =250, activebackground= Blue_Salvia, highlightbackground=Yellow_Sulphur, troughcolor= Yellow_Sulphur, orient=HORIZONTAL)
    Track_C6_Volume_SLIDER.place(relx = 0.70, rely = 0.75, anchor = CENTER)

    #Midi Info stuff.

    Title_label = Label(newWindow, text=("Track {} original title:".format(id)),bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
    Title_label.config(font=(Font_UI, 10, BOLD))
    Title_label.place(relx = 0.178, rely = 0.05, anchor = CENTER)

    Track_title = Entry(newWindow, font=(Font_UI, 8, BOLD), bg = Blue_Salvia, borderwidth=2, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
    Track_title.place(relx = 0.71, rely = 0.05, anchor = CENTER, width= 250)
    Track_title.insert(END,Title)
    Track_title.config(state="readonly")

    Instrument_label = Label(newWindow, text=("Track {} original instrument:".format(id)),bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
    Instrument_label.config(font=(Font_UI, 10, BOLD))
    Instrument_label.place(relx = 0.22, rely = 0.12, anchor = CENTER)

    Instrument_title = Entry(newWindow, font=(Font_UI, 8, BOLD), bg = Blue_Salvia, borderwidth=2, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
    Instrument_title.place(relx = 0.71, rely = 0.12, anchor = CENTER, width=250)
    Instrument_title.insert(END,Instrument)
    Instrument_title.config(state="readonly")

    def Apply_changes(id):

        Volume_Value=Track_Volume_SLIDER.get()
        Panning_Value=Track_Panning_SLIDER.get()
        Instrument_Value=InstrumentSelectBox.get()
        try:
            Instrument_Value=(Intrument_Groups.ID_instrument_List[Instrument_Value])
             
            Track_C6_Volume_Value = Track_C6_Volume_SLIDER.get()

            if id == 0:
                Track_0_Volume.config(state="normal")
                Track_0_Volume.delete(0, END)
                Track_0_Volume.insert(END,Volume_Value)
                Track_0_Volume.config(state="readonly")

                Track_0_Pan.config(state="normal")
                Track_0_Pan.delete(0, END)
                Track_0_Pan.insert(END, Panning_Value)
                Track_0_Pan.config(state="readonly")

                Track_0_Instrument.config(state="normal")
                Track_0_Instrument.delete(0, END)
                Track_0_Instrument.insert(END, Instrument_Value)
                Track_0_Instrument.config(state="readonly")

                Track_0_C6_Value.config(state="normal")
                Track_0_C6_Value.delete(0, END)
                Track_0_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_0_C6_Value.config(state="readonly")
            elif id == 1:
                Track_1_Volume.config(state="normal")
                Track_1_Volume.delete(0, END)
                Track_1_Volume.insert(END,Volume_Value)
                Track_1_Volume.config(state="readonly")

                Track_1_Pan.config(state="normal")
                Track_1_Pan.delete(0, END)
                Track_1_Pan.insert(END, Panning_Value)
                Track_1_Pan.config(state="readonly")

                Track_1_Instrument.config(state="normal")
                Track_1_Instrument.delete(0, END)
                Track_1_Instrument.insert(END, Instrument_Value)
                Track_1_Instrument.config(state="readonly")

                Track_1_C6_Value.config(state="normal")
                Track_1_C6_Value.delete(0, END)
                Track_1_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_1_C6_Value.config(state="readonly")
            elif id == 2:
                Track_2_Volume.config(state="normal")
                Track_2_Volume.delete(0, END)
                Track_2_Volume.insert(END,Volume_Value)
                Track_2_Volume.config(state="readonly")

                Track_2_Pan.config(state="normal")
                Track_2_Pan.delete(0, END)
                Track_2_Pan.insert(END, Panning_Value)
                Track_2_Pan.config(state="readonly")

                Track_2_Instrument.config(state="normal")
                Track_2_Instrument.delete(0, END)
                Track_2_Instrument.insert(END, Instrument_Value)
                Track_2_Instrument.config(state="readonly")

                Track_2_C6_Value.config(state="normal")
                Track_2_C6_Value.delete(0, END)
                Track_2_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_2_C6_Value.config(state="readonly")
            elif id == 3:
                Track_3_Volume.config(state="normal")
                Track_3_Volume.delete(0, END)
                Track_3_Volume.insert(END,Volume_Value)
                Track_3_Volume.config(state="readonly")

                Track_3_Pan.config(state="normal")
                Track_3_Pan.delete(0, END)
                Track_3_Pan.insert(END, Panning_Value)
                Track_3_Pan.config(state="readonly")

                Track_3_Instrument.config(state="normal")
                Track_3_Instrument.delete(0, END)
                Track_3_Instrument.insert(END, Instrument_Value)
                Track_3_Instrument.config(state="readonly")

                Track_3_C6_Value.config(state="normal")
                Track_3_C6_Value.delete(0, END)
                Track_3_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_3_C6_Value.config(state="readonly")
            elif id == 4:
                Track_4_Volume.config(state="normal")
                Track_4_Volume.delete(0, END)
                Track_4_Volume.insert(END,Volume_Value)
                Track_4_Volume.config(state="readonly")

                Track_4_Pan.config(state="normal")
                Track_4_Pan.delete(0, END)
                Track_4_Pan.insert(END, Panning_Value)
                Track_4_Pan.config(state="readonly")

                Track_4_Instrument.config(state="normal")
                Track_4_Instrument.delete(0, END)
                Track_4_Instrument.insert(END, Instrument_Value)
                Track_4_Instrument.config(state="readonly")

                Track_4_C6_Value.config(state="normal")
                Track_4_C6_Value.delete(0, END)
                Track_4_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_4_C6_Value.config(state="readonly")
            elif id == 5:
                Track_5_Volume.config(state="normal")
                Track_5_Volume.delete(0, END)
                Track_5_Volume.insert(END,Volume_Value)
                Track_5_Volume.config(state="readonly")

                Track_5_Pan.config(state="normal")
                Track_5_Pan.delete(0, END)
                Track_5_Pan.insert(END, Panning_Value)
                Track_5_Pan.config(state="readonly")

                Track_5_Instrument.config(state="normal")
                Track_5_Instrument.delete(0, END)
                Track_5_Instrument.insert(END, Instrument_Value)
                Track_5_Instrument.config(state="readonly")

                Track_5_C6_Value.config(state="normal")
                Track_5_C6_Value.delete(0, END)
                Track_5_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_5_C6_Value.config(state="readonly")
            elif id == 6:
                Track_6_Volume.config(state="normal")
                Track_6_Volume.delete(0, END)
                Track_6_Volume.insert(END,Volume_Value)
                Track_6_Volume.config(state="readonly")

                Track_6_Pan.config(state="normal")
                Track_6_Pan.delete(0, END)
                Track_6_Pan.insert(END, Panning_Value)
                Track_6_Pan.config(state="readonly")

                Track_6_Instrument.config(state="normal")
                Track_6_Instrument.delete(0, END)
                Track_6_Instrument.insert(END, Instrument_Value)
                Track_6_Instrument.config(state="readonly")

                Track_6_C6_Value.config(state="normal")
                Track_6_C6_Value.delete(0, END)
                Track_6_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_6_C6_Value.config(state="readonly")
            elif id == 7:
                Track_7_Volume.config(state="normal")
                Track_7_Volume.delete(0, END)
                Track_7_Volume.insert(END,Volume_Value)
                Track_7_Volume.config(state="readonly")

                Track_7_Pan.config(state="normal")
                Track_7_Pan.delete(0, END)
                Track_7_Pan.insert(END, Panning_Value)
                Track_7_Pan.config(state="readonly")

                Track_7_Instrument.config(state="normal")
                Track_7_Instrument.delete(0, END)
                Track_7_Instrument.insert(END, Instrument_Value)
                Track_7_Instrument.config(state="readonly")

                Track_7_C6_Value.config(state="normal")
                Track_7_C6_Value.delete(0, END)
                Track_7_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_7_C6_Value.config(state="readonly")
            elif id == 8:
                Track_8_Volume.config(state="normal")
                Track_8_Volume.delete(0, END)
                Track_8_Volume.insert(END,Volume_Value)
                Track_8_Volume.config(state="readonly")

                Track_8_Pan.config(state="normal")
                Track_8_Pan.delete(0, END)
                Track_8_Pan.insert(END, Panning_Value)
                Track_8_Pan.config(state="readonly")

                Track_8_Instrument.config(state="normal")
                Track_8_Instrument.delete(0, END)
                Track_8_Instrument.insert(END, Instrument_Value)
                Track_8_Instrument.config(state="readonly")

                Track_8_C6_Value.config(state="normal")
                Track_8_C6_Value.delete(0, END)
                Track_8_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_8_C6_Value.config(state="readonly")
            elif id == 9:
                Track_9_Volume.config(state="normal")
                Track_9_Volume.delete(0, END)
                Track_9_Volume.insert(END,Volume_Value)
                Track_9_Volume.config(state="readonly")

                Track_9_Pan.config(state="normal")
                Track_9_Pan.delete(0, END)
                Track_9_Pan.insert(END, Panning_Value)
                Track_9_Pan.config(state="readonly")

                Track_9_Instrument.config(state="normal")
                Track_9_Instrument.delete(0, END)
                Track_9_Instrument.insert(END, Instrument_Value)
                Track_9_Instrument.config(state="readonly")

                Track_9_C6_Value.config(state="normal")
                Track_9_C6_Value.delete(0, END)
                Track_9_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_9_C6_Value.config(state="readonly")
            elif id == 10:
                Track_10_Volume.config(state="normal")
                Track_10_Volume.delete(0, END)
                Track_10_Volume.insert(END,Volume_Value)
                Track_10_Volume.config(state="readonly")

                Track_10_Pan.config(state="normal")
                Track_10_Pan.delete(0, END)
                Track_10_Pan.insert(END, Panning_Value)
                Track_10_Pan.config(state="readonly")

                Track_10_Instrument.config(state="normal")
                Track_10_Instrument.delete(0, END)
                Track_10_Instrument.insert(END, Instrument_Value)
                Track_10_Instrument.config(state="readonly")

                Track_10_C6_Value.config(state="normal")
                Track_10_C6_Value.delete(0, END)
                Track_10_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_10_C6_Value.config(state="readonly")
            elif id == 11:
                Track_11_Volume.config(state="normal")
                Track_11_Volume.delete(0, END)
                Track_11_Volume.insert(END,Volume_Value)
                Track_11_Volume.config(state="readonly")

                Track_11_Pan.config(state="normal")
                Track_11_Pan.delete(0, END)
                Track_11_Pan.insert(END, Panning_Value)
                Track_11_Pan.config(state="readonly")

                Track_11_Instrument.config(state="normal")
                Track_11_Instrument.delete(0, END)
                Track_11_Instrument.insert(END, Instrument_Value)
                Track_11_Instrument.config(state="readonly")

                Track_11_C6_Value.config(state="normal")
                Track_11_C6_Value.delete(0, END)
                Track_11_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_11_C6_Value.config(state="readonly")
            elif id == 12:
                Track_12_Volume.config(state="normal")
                Track_12_Volume.delete(0, END)
                Track_12_Volume.insert(END,Volume_Value)
                Track_12_Volume.config(state="readonly")

                Track_12_Pan.config(state="normal")
                Track_12_Pan.delete(0, END)
                Track_12_Pan.insert(END, Panning_Value)
                Track_12_Pan.config(state="readonly")

                Track_12_Instrument.config(state="normal")
                Track_12_Instrument.delete(0, END)
                Track_12_Instrument.insert(END, Instrument_Value)
                Track_12_Instrument.config(state="readonly")

                Track_12_C6_Value.config(state="normal")
                Track_12_C6_Value.delete(0, END)
                Track_12_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_12_C6_Value.config(state="readonly")
            elif id == 13:
                Track_13_Volume.config(state="normal")
                Track_13_Volume.delete(0, END)
                Track_13_Volume.insert(END,Volume_Value)
                Track_13_Volume.config(state="readonly")

                Track_13_Pan.config(state="normal")
                Track_13_Pan.delete(0, END)
                Track_13_Pan.insert(END, Panning_Value)
                Track_13_Pan.config(state="readonly")

                Track_13_Instrument.config(state="normal")
                Track_13_Instrument.delete(0, END)
                Track_13_Instrument.insert(END, Instrument_Value)
                Track_13_Instrument.config(state="readonly")

                Track_13_C6_Value.config(state="normal")
                Track_13_C6_Value.delete(0, END)
                Track_13_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_13_C6_Value.config(state="readonly")
            elif id == 14:
                Track_14_Volume.config(state="normal")
                Track_14_Volume.delete(0, END)
                Track_14_Volume.insert(END,Volume_Value)
                Track_14_Volume.config(state="readonly")

                Track_14_Pan.config(state="normal")
                Track_14_Pan.delete(0, END)
                Track_14_Pan.insert(END, Panning_Value)
                Track_14_Pan.config(state="readonly")

                Track_14_Instrument.config(state="normal")
                Track_14_Instrument.delete(0, END)
                Track_14_Instrument.insert(END, Instrument_Value)
                Track_14_Instrument.config(state="readonly")

                Track_14_C6_Value.config(state="normal")
                Track_14_C6_Value.delete(0, END)
                Track_14_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_14_C6_Value.config(state="readonly")
            elif id == 15:
                Track_15_Volume.config(state="normal")
                Track_15_Volume.delete(0, END)
                Track_15_Volume.insert(END,Volume_Value)
                Track_15_Volume.config(state="readonly")

                Track_15_Pan.config(state="normal")
                Track_15_Pan.delete(0, END)
                Track_15_Pan.insert(END, Panning_Value)
                Track_15_Pan.config(state="readonly")

                Track_15_Instrument.config(state="normal")
                Track_15_Instrument.delete(0, END)
                Track_15_Instrument.insert(END, Instrument_Value)
                Track_15_Instrument.config(state="readonly")

                Track_15_C6_Value.config(state="normal")
                Track_15_C6_Value.delete(0, END)
                Track_15_C6_Value.insert(END, Track_C6_Volume_Value)
                Track_15_C6_Value.config(state="readonly")
        except KeyError: 
            messagebox.showerror(title="Bank error! (ERROR ID:21)", message="Please, do not switch games while this window is open.")
    Track_apply_Button = Button(newWindow, text="Apply changes",bg= Blue_Salvia, fg= Dark_Olive_Slate)
    Track_apply_Button.config(command= lambda: Apply_changes(id))
    Track_apply_Button.place(relx = 0.2, rely = (0.90), anchor = CENTER, width=100,  height= 45)

class Info_buttons:
    
    Track_0_info_Button = Button(root, text="Track 00:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_0_info_Button.config(command= lambda: openNewWindow(0,Track_Information_lookup.Track_0_OG_Track_name,Track_Information_lookup.Track_0_OG_Intrument))
    Track_0_info_Button.place(relx = 0.1, rely = (0.31), anchor = CENTER, width=50,  height= 19)

    Track_1_info_Button = Button(root, text="Track 01:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_1_info_Button.config(command= lambda: openNewWindow(1,Track_Information_lookup.Track_1_OG_Track_name,Track_Information_lookup.Track_1_OG_Intrument))
    Track_1_info_Button.place(relx = 0.1, rely = (0.352), anchor = CENTER, width=50,  height= 19)

    Track_3_info_Button = Button(root, text="Track 02:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_3_info_Button.config(command= lambda: openNewWindow(2,Track_Information_lookup.Track_2_OG_Track_name,Track_Information_lookup.Track_2_OG_Intrument))
    Track_3_info_Button.place(relx = 0.1, rely = (0.394), anchor = CENTER, width=50,  height= 19)

    Track_4_info_Button = Button(root, text="Track 03:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_4_info_Button.config(command= lambda: openNewWindow(3,Track_Information_lookup.Track_3_OG_Track_name,Track_Information_lookup.Track_3_OG_Intrument))
    Track_4_info_Button.place(relx = 0.1, rely = (0.436), anchor = CENTER, width=50,  height= 19)

    Track_5_info_Button = Button(root, text="Track 04:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_5_info_Button.config(command= lambda: openNewWindow(4,Track_Information_lookup.Track_4_OG_Track_name,Track_Information_lookup.Track_4_OG_Intrument))
    Track_5_info_Button.place(relx = 0.1, rely = (0.478), anchor = CENTER, width=50,  height= 19)

    Track_6_info_Button = Button(root, text="Track 05:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_6_info_Button.config(command= lambda: openNewWindow(5,Track_Information_lookup.Track_5_OG_Track_name,Track_Information_lookup.Track_5_OG_Intrument))
    Track_6_info_Button.place(relx = 0.1, rely = (0.52), anchor = CENTER, width=50,  height= 19)

    Track_7_info_Button = Button(root, text="Track 06:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_7_info_Button.config(command= lambda: openNewWindow(6,Track_Information_lookup.Track_6_OG_Track_name,Track_Information_lookup.Track_6_OG_Intrument))
    Track_7_info_Button.place(relx = 0.1, rely = (0.562), anchor = CENTER, width=50,  height= 19)

    Track_8_info_Button = Button(root, text="Track 07:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_8_info_Button.config(command= lambda: openNewWindow(7,Track_Information_lookup.Track_7_OG_Track_name,Track_Information_lookup.Track_7_OG_Intrument))
    Track_8_info_Button.place(relx = 0.1, rely = (0.604), anchor = CENTER, width=50,  height= 19)

    Track_9_info_Button = Button(root, text="Track 08:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_9_info_Button.config(command= lambda: openNewWindow(8,Track_Information_lookup.Track_8_OG_Track_name,Track_Information_lookup.Track_8_OG_Intrument))
    Track_9_info_Button.place(relx = 0.1, rely = (0.646), anchor = CENTER, width=50,  height= 19)

    Track_10_info_Button = Button(root, text="Track 09:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_10_info_Button.config(command= lambda: openNewWindow(9,Track_Information_lookup.Track_9_OG_Track_name,Track_Information_lookup.Track_9_OG_Intrument))
    Track_10_info_Button.place(relx = 0.1, rely = (0.688), anchor = CENTER, width=50,  height= 19)

    Track_11_info_Button = Button(root, text="Track 10:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_11_info_Button.config(command= lambda: openNewWindow(10,Track_Information_lookup.Track_10_OG_Track_name,Track_Information_lookup.Track_10_OG_Intrument))
    Track_11_info_Button.place(relx = 0.1, rely = (0.73), anchor = CENTER, width=50,  height= 19)

    Track_12_info_Button = Button(root, text="Track 11:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_12_info_Button.config(command= lambda: openNewWindow(11,Track_Information_lookup.Track_11_OG_Track_name,Track_Information_lookup.Track_11_OG_Intrument))
    Track_12_info_Button.place(relx = 0.1, rely = (0.772), anchor = CENTER, width=50,  height= 19)

    Track_13_info_Button = Button(root, text="Track 12:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_13_info_Button.config(command= lambda: openNewWindow(12,Track_Information_lookup.Track_12_OG_Track_name,Track_Information_lookup.Track_12_OG_Intrument))
    Track_13_info_Button.place(relx = 0.1, rely = (0.814), anchor = CENTER, width=50,  height= 19)

    Track_14_info_Button = Button(root, text="Track 13:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_14_info_Button.config(command= lambda: openNewWindow(13,Track_Information_lookup.Track_13_OG_Track_name,Track_Information_lookup.Track_13_OG_Intrument))
    Track_14_info_Button.place(relx = 0.1, rely = (0.856), anchor = CENTER, width=50,  height= 19)

    Track_15_info_Button = Button(root, text="Track 14:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_15_info_Button.config(command= lambda: openNewWindow(14,Track_Information_lookup.Track_14_OG_Track_name,Track_Information_lookup.Track_14_OG_Intrument))
    Track_15_info_Button.place(relx = 0.1, rely = (0.898), anchor = CENTER, width=50,  height= 19)

    Track_16_info_Button = Button(root, text="Track 15:",font=(Font_UI, 8, BOLD), bg= Dark_Olive_Slate, fg= Yellow_Sulphur, borderwidth= 0)
    Track_16_info_Button.config(command= lambda: openNewWindow(15,Track_Information_lookup.Track_15_OG_Track_name,Track_Information_lookup.Track_15_OG_Intrument))
    Track_16_info_Button.place(relx = 0.1, rely = (0.94), anchor = CENTER, width=50,  height= 19)

def Save_instrument_layout():
    Layout_list = []
    Track_layout_List = []
    Track_layout_List.append(Track_0_Volume.get())
    Track_layout_List.append(Track_0_Instrument.get())
    Track_layout_List.append(Track_0_Pan.get())
    Track_layout_List.append(Track_0_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_1_Volume.get())
    Track_layout_List.append(Track_1_Instrument.get())
    Track_layout_List.append(Track_1_Pan.get())
    Track_layout_List.append(Track_1_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_2_Volume.get())
    Track_layout_List.append(Track_2_Instrument.get())
    Track_layout_List.append(Track_2_Pan.get())
    Track_layout_List.append(Track_2_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_3_Volume.get())
    Track_layout_List.append(Track_3_Instrument.get())
    Track_layout_List.append(Track_3_Pan.get())
    Track_layout_List.append(Track_3_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_4_Volume.get())
    Track_layout_List.append(Track_4_Instrument.get())
    Track_layout_List.append(Track_4_Pan.get())
    Track_layout_List.append(Track_4_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_5_Volume.get())
    Track_layout_List.append(Track_5_Instrument.get())
    Track_layout_List.append(Track_5_Pan.get())
    Track_layout_List.append(Track_5_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_6_Volume.get())
    Track_layout_List.append(Track_6_Instrument.get())
    Track_layout_List.append(Track_6_Pan.get())
    Track_layout_List.append(Track_6_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_7_Volume.get())
    Track_layout_List.append(Track_7_Instrument.get())
    Track_layout_List.append(Track_7_Pan.get())
    Track_layout_List.append(Track_7_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_8_Volume.get())
    Track_layout_List.append(Track_8_Instrument.get())
    Track_layout_List.append(Track_8_Pan.get())
    Track_layout_List.append(Track_8_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_9_Volume.get())
    Track_layout_List.append(Track_9_Instrument.get())
    Track_layout_List.append(Track_9_Pan.get())
    Track_layout_List.append(Track_9_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_10_Volume.get())
    Track_layout_List.append(Track_10_Instrument.get())
    Track_layout_List.append(Track_10_Pan.get())
    Track_layout_List.append(Track_10_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_11_Volume.get())
    Track_layout_List.append(Track_11_Instrument.get())
    Track_layout_List.append(Track_11_Pan.get())
    Track_layout_List.append(Track_11_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_12_Volume.get())
    Track_layout_List.append(Track_12_Instrument.get())
    Track_layout_List.append(Track_12_Pan.get())
    Track_layout_List.append(Track_12_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_13_Volume.get())
    Track_layout_List.append(Track_13_Instrument.get())
    Track_layout_List.append(Track_13_Pan.get())
    Track_layout_List.append(Track_13_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_14_Volume.get())
    Track_layout_List.append(Track_14_Instrument.get())
    Track_layout_List.append(Track_14_Pan.get())
    Track_layout_List.append(Track_14_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(Track_15_Volume.get())
    Track_layout_List.append(Track_15_Instrument.get())
    Track_layout_List.append(Track_15_Pan.get())
    Track_layout_List.append(Track_15_C6_Value.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []
    Track_layout_List.append(BPM_multiplier_Entry.get())
    Layout_list.append(Track_layout_List)
    Track_layout_List = []


    save_file = filedialog.asksaveasfilename(initialdir = "/",title = "Select where to save your file.",filetypes = [(".doot files","*.doot")])
    save_file = save_file.replace(".doot","")
    out_file = open(f"{save_file}.doot", "w+")
    out_file.write(str(Layout_list))
    out_file.close
    TK_Message("Layout Saved!","Roar!")

def Load_instrument_layout():
    Imported_file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [(".doot files","*.doot"), ("all files","*.*")])
    with open(Imported_file, "r") as opened_file:
        data = opened_file.read()
        data = ast.literal_eval(data)
        class Set_entry_values:
            Track_0_Volume.config(state="normal")
            Track_0_Volume.delete(0, END)
            Track_0_Volume.insert(END,data[0][0])
            Track_0_Volume.config(state="readonly")
            
            Track_0_Pan.config(state="normal")
            Track_0_Pan.delete(0, END)
            Track_0_Pan.insert(END,data[0][2])
            Track_0_Pan.config(state="readonly")

            Track_0_Instrument.config(state="normal")
            Track_0_Instrument.delete(0, END)
            Track_0_Instrument.insert(END,data[0][1])
            Track_0_Instrument.config(state="readonly")

            Track_0_C6_Value.config(state="normal")
            Track_0_C6_Value.delete(0, END)
            Track_0_C6_Value.insert(END,data[0][3])
            Track_0_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_1_Volume.config(state="normal")
            Track_1_Volume.delete(0, END)
            Track_1_Volume.insert(END,data[1][0])
            Track_1_Volume.config(state="readonly")
            
            Track_1_Pan.config(state="normal")
            Track_1_Pan.delete(0, END)
            Track_1_Pan.insert(END,data[1][2])
            Track_1_Pan.config(state="readonly")

            Track_1_Instrument.config(state="normal")
            Track_1_Instrument.delete(0, END)
            Track_1_Instrument.insert(END,data[1][1])
            Track_1_Instrument.config(state="readonly")

            Track_1_C6_Value.config(state="normal")
            Track_1_C6_Value.delete(0, END)
            Track_1_C6_Value.insert(END,data[1][3])
            Track_1_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_2_Volume.config(state="normal")
            Track_2_Volume.delete(0, END)
            Track_2_Volume.insert(END,data[2][0])
            Track_2_Volume.config(state="readonly")
            
            Track_2_Pan.config(state="normal")
            Track_2_Pan.delete(0, END)
            Track_2_Pan.insert(END,data[2][2])
            Track_2_Pan.config(state="readonly")

            Track_2_Instrument.config(state="normal")
            Track_2_Instrument.delete(0, END)
            Track_2_Instrument.insert(END,data[2][1])
            Track_2_Instrument.config(state="readonly")

            Track_2_C6_Value.config(state="normal")
            Track_2_C6_Value.delete(0, END)
            Track_2_C6_Value.insert(END,data[2][3])
            Track_2_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_3_Volume.config(state="normal")
            Track_3_Volume.delete(0, END)
            Track_3_Volume.insert(END,data[3][0])
            Track_3_Volume.config(state="readonly")
            
            Track_3_Pan.config(state="normal")
            Track_3_Pan.delete(0, END)
            Track_3_Pan.insert(END,data[3][2])
            Track_3_Pan.config(state="readonly")

            Track_3_Instrument.config(state="normal")
            Track_3_Instrument.delete(0, END)
            Track_3_Instrument.insert(END,data[3][1])
            Track_3_Instrument.config(state="readonly")

            Track_3_C6_Value.config(state="normal")
            Track_3_C6_Value.delete(0, END)
            Track_3_C6_Value.insert(END,data[3][3])
            Track_3_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_4_Volume.config(state="normal")
            Track_4_Volume.delete(0, END)
            Track_4_Volume.insert(END,data[4][0])
            Track_4_Volume.config(state="readonly")
            
            Track_4_Pan.config(state="normal")
            Track_4_Pan.delete(0, END)
            Track_4_Pan.insert(END,data[4][2])
            Track_4_Pan.config(state="readonly")

            Track_4_Instrument.config(state="normal")
            Track_4_Instrument.delete(0, END)
            Track_4_Instrument.insert(END,data[4][1])
            Track_4_Instrument.config(state="readonly")

            Track_4_C6_Value.config(state="normal")
            Track_4_C6_Value.delete(0, END)
            Track_4_C6_Value.insert(END,data[4][3])
            Track_4_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_5_Volume.config(state="normal")
            Track_5_Volume.delete(0, END)
            Track_5_Volume.insert(END,data[5][0])
            Track_5_Volume.config(state="readonly")
            
            Track_5_Pan.config(state="normal")
            Track_5_Pan.delete(0, END)
            Track_5_Pan.insert(END,data[5][2])
            Track_5_Pan.config(state="readonly")

            Track_5_Instrument.config(state="normal")
            Track_5_Instrument.delete(0, END)
            Track_5_Instrument.insert(END,data[5][1])
            Track_5_Instrument.config(state="readonly")

            Track_5_C6_Value.config(state="normal")
            Track_5_C6_Value.delete(0, END)
            Track_5_C6_Value.insert(END,data[5][3])
            Track_5_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_6_Volume.config(state="normal")
            Track_6_Volume.delete(0, END)
            Track_6_Volume.insert(END,data[6][0])
            Track_6_Volume.config(state="readonly")
            
            Track_6_Pan.config(state="normal")
            Track_6_Pan.delete(0, END)
            Track_6_Pan.insert(END,data[6][2])
            Track_6_Pan.config(state="readonly")

            Track_6_Instrument.config(state="normal")
            Track_6_Instrument.delete(0, END)
            Track_6_Instrument.insert(END,data[6][1])
            Track_6_Instrument.config(state="readonly")

            Track_6_C6_Value.config(state="normal")
            Track_6_C6_Value.delete(0, END)
            Track_6_C6_Value.insert(END,data[6][3])
            Track_6_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_7_Volume.config(state="normal")
            Track_7_Volume.delete(0, END)
            Track_7_Volume.insert(END,data[7][0])
            Track_7_Volume.config(state="readonly")
            
            Track_7_Pan.config(state="normal")
            Track_7_Pan.delete(0, END)
            Track_7_Pan.insert(END,data[7][2])
            Track_7_Pan.config(state="readonly")

            Track_7_Instrument.config(state="normal")
            Track_7_Instrument.delete(0, END)
            Track_7_Instrument.insert(END,data[7][1])
            Track_7_Instrument.config(state="readonly")

            Track_7_C6_Value.config(state="normal")
            Track_7_C6_Value.delete(0, END)
            Track_7_C6_Value.insert(END,data[7][3])
            Track_7_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_8_Volume.config(state="normal")
            Track_8_Volume.delete(0, END)
            Track_8_Volume.insert(END,data[8][0])
            Track_8_Volume.config(state="readonly")
            
            Track_8_Pan.config(state="normal")
            Track_8_Pan.delete(0, END)
            Track_8_Pan.insert(END,data[8][2])
            Track_8_Pan.config(state="readonly")

            Track_8_Instrument.config(state="normal")
            Track_8_Instrument.delete(0, END)
            Track_8_Instrument.insert(END,data[8][1])
            Track_8_Instrument.config(state="readonly")

            Track_8_C6_Value.config(state="normal")
            Track_8_C6_Value.delete(0, END)
            Track_8_C6_Value.insert(END,data[8][3])
            Track_8_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_9_Volume.config(state="normal")
            Track_9_Volume.delete(0, END)
            Track_9_Volume.insert(END,data[9][0])
            Track_9_Volume.config(state="readonly")
            
            Track_9_Pan.config(state="normal")
            Track_9_Pan.delete(0, END)
            Track_9_Pan.insert(END,data[9][2])
            Track_9_Pan.config(state="readonly")

            Track_9_Instrument.config(state="normal")
            Track_9_Instrument.delete(0, END)
            Track_9_Instrument.insert(END,data[9][1])
            Track_9_Instrument.config(state="readonly")

            Track_9_C6_Value.config(state="normal")
            Track_9_C6_Value.delete(0, END)
            Track_9_C6_Value.insert(END,data[9][3])
            Track_9_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_10_Volume.config(state="normal")
            Track_10_Volume.delete(0, END)
            Track_10_Volume.insert(END,data[10][0])
            Track_10_Volume.config(state="readonly")
            
            Track_10_Pan.config(state="normal")
            Track_10_Pan.delete(0, END)
            Track_10_Pan.insert(END,data[10][2])
            Track_10_Pan.config(state="readonly")

            Track_10_Instrument.config(state="normal")
            Track_10_Instrument.delete(0, END)
            Track_10_Instrument.insert(END,data[10][1])
            Track_10_Instrument.config(state="readonly")

            Track_10_C6_Value.config(state="normal")
            Track_10_C6_Value.delete(0, END)
            Track_10_C6_Value.insert(END,data[10][3])
            Track_10_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_11_Volume.config(state="normal")
            Track_11_Volume.delete(0, END)
            Track_11_Volume.insert(END,data[11][0])
            Track_11_Volume.config(state="readonly")
            
            Track_11_Pan.config(state="normal")
            Track_11_Pan.delete(0, END)
            Track_11_Pan.insert(END,data[11][2])
            Track_11_Pan.config(state="readonly")

            Track_11_Instrument.config(state="normal")
            Track_11_Instrument.delete(0, END)
            Track_11_Instrument.insert(END,data[11][1])
            Track_11_Instrument.config(state="readonly")

            Track_11_C6_Value.config(state="normal")
            Track_11_C6_Value.delete(0, END)
            Track_11_C6_Value.insert(END,data[11][3])
            Track_11_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_12_Volume.config(state="normal")
            Track_12_Volume.delete(0, END)
            Track_12_Volume.insert(END,data[12][0])
            Track_12_Volume.config(state="readonly")
            
            Track_12_Pan.config(state="normal")
            Track_12_Pan.delete(0, END)
            Track_12_Pan.insert(END,data[12][2])
            Track_12_Pan.config(state="readonly")

            Track_12_Instrument.config(state="normal")
            Track_12_Instrument.delete(0, END)
            Track_12_Instrument.insert(END,data[12][1])
            Track_12_Instrument.config(state="readonly")

            Track_12_C6_Value.config(state="normal")
            Track_12_C6_Value.delete(0, END)
            Track_12_C6_Value.insert(END,data[12][3])
            Track_12_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_13_Volume.config(state="normal")
            Track_13_Volume.delete(0, END)
            Track_13_Volume.insert(END,data[13][0])
            Track_13_Volume.config(state="readonly")
            
            Track_13_Pan.config(state="normal")
            Track_13_Pan.delete(0, END)
            Track_13_Pan.insert(END,data[13][2])
            Track_13_Pan.config(state="readonly")

            Track_13_Instrument.config(state="normal")
            Track_13_Instrument.delete(0, END)
            Track_13_Instrument.insert(END,data[13][1])
            Track_13_Instrument.config(state="readonly")

            Track_13_C6_Value.config(state="normal")
            Track_13_C6_Value.delete(0, END)
            Track_13_C6_Value.insert(END,data[13][3])
            Track_13_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_14_Volume.config(state="normal")
            Track_14_Volume.delete(0, END)
            Track_14_Volume.insert(END,data[14][0])
            Track_14_Volume.config(state="readonly")
            
            Track_14_Pan.config(state="normal")
            Track_14_Pan.delete(0, END)
            Track_14_Pan.insert(END,data[14][2])
            Track_14_Pan.config(state="readonly")

            Track_14_Instrument.config(state="normal")
            Track_14_Instrument.delete(0, END)
            Track_14_Instrument.insert(END,data[14][1])
            Track_14_Instrument.config(state="readonly")

            Track_14_C6_Value.config(state="normal")
            Track_14_C6_Value.delete(0, END)
            Track_14_C6_Value.insert(END,data[14][3])
            Track_14_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            Track_15_Volume.config(state="normal")
            Track_15_Volume.delete(0, END)
            Track_15_Volume.insert(END,data[15][0])
            Track_15_Volume.config(state="readonly")
            
            Track_15_Pan.config(state="normal")
            Track_15_Pan.delete(0, END)
            Track_15_Pan.insert(END,data[15][2])
            Track_15_Pan.config(state="readonly")

            Track_15_Instrument.config(state="normal")
            Track_15_Instrument.delete(0, END)
            Track_15_Instrument.insert(END,data[15][1])
            Track_15_Instrument.config(state="readonly")

            Track_15_C6_Value.config(state="normal")
            Track_15_C6_Value.delete(0, END)
            Track_15_C6_Value.insert(END,data[15][3])
            Track_15_C6_Value.config(state="readonly")

            #/////////////////////////////////////////
            BPM_multiplier_Entry.delete(0, END)
            BPM_multiplier_Entry.insert(END,data[16][0])
                      
    opened_file.close()    


#Beginning_Byte_Entry = Entry(root, state="normal",bg = Blue_Salvia, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
#Beginning_Byte_Entry.insert (END,"0")
#Beginning_Byte_Entry.place(relx = 0.5, rely = 0.45, anchor = CENTER, width=25)


BPM_Entry = Entry(root, state="readonly",font=(Font_UI, 13, BOLD),justify='center',bg = Blue_Salvia, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
BPM_Entry.place(relx = 0.87, rely = 0.40, anchor = CENTER, width=40, height=35)

BPM_multiplier_Entry = Entry(root, state="normal",font=(Font_UI, 13, BOLD),justify='center',bg = Blue_Salvia, highlightbackground=Yellow_Sulphur, fg = Dark_Olive_Slate)
BPM_multiplier_Entry.insert(END, "16.9")
BPM_multiplier_Entry.place(relx = 0.71, rely = 0.40, anchor = CENTER, width=40, height=35)

Input_Box_message_GAME = Label(root, text="Game:",bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
Input_Box_message_GAME.config(font=(Font_UI, 8, BOLD))
Input_Box_message_GAME.place(relx = 0.71, rely = 0.48, anchor = CENTER)

#def Combobox_change_instrument_bank(self):
#    Bank_ID = self.get()
#    print(Bank_ID)

def Combobox_change_instrument_bank(event):
    Game_name = (Game_combo_box.get())

    if str(Game_name) == "HFTF":
        Intrument_Groups.ID_instrument_List = ID_instrument_List_HFTF
        Intrument_Groups.ID_instrument_items = ID_instrument_items_HFTF
    elif str(Game_name) == "Red Earth":
        Intrument_Groups.ID_instrument_List = ID_instrument_List_RED
        Intrument_Groups.ID_instrument_items = ID_instrument_items_RED 
    elif str(Game_name) == "SFIII: New generation":
        messagebox.showwarning(title="Missing Instrument Bank", message="Sorry but this game is not supported yet.")
    elif str(Game_name) == "SFIII: Second Impact":
        messagebox.showwarning(title="Missing Instrument Bank", message="Sorry but this game is not supported yet.")
    elif str(Game_name) == "SFIII: Third Strike":
        Intrument_Groups.ID_instrument_List = ID_instrument_List_3S
        Intrument_Groups.ID_instrument_items = ID_instrument_items_3S                 


Game_combo_box = ttk.Combobox(root, values=["HFTF","Red Earth","SFIII: New generation","SFIII: Second Impact","SFIII: Third Strike"])
Game_combo_box.config(font=(Font_UI, 7, BOLD),width= "10",state="readonly")
Game_combo_box.place(relx = 0.71, rely = 0.58, anchor = CENTER)
Game_combo_box.current(0)
Game_combo_box.bind("<<ComboboxSelected>>", Combobox_change_instrument_bank)


#Slider

Pitch_shift_slider = Scale(root, from_= +20, to=-20)
Pitch_shift_slider.set(0)
Pitch_shift_slider.config(bg = Blue_Salvia, fg = Dark_Olive_Slate, borderwidth= (2), tickinterval=8, length =100, activebackground= Blue_Salvia, highlightbackground=Yellow_Sulphur, troughcolor= Yellow_Sulphur)
Pitch_shift_slider.place(relx = 0.87, rely = 0.682, anchor = CENTER)

#Labels

Input_Box_message1 = Label(root, text="Open MIDI raw data",bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
Input_Box_message1.config(font=(Font_UI, 10, BOLD))
Input_Box_message1.place(relx = 0.75, rely = 0.11, anchor = CENTER)

Input_Box_message2 = Label(root, text="Output",bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
Input_Box_message2.config(font=(Font_UI, 10, BOLD))
Input_Box_message2.place(relx = 0.27, rely = 0.11, anchor = CENTER)

Track_0_info_Button = Label(root, text="Tempo Multiplier:     Tempo (BMP):",bg= Dark_Olive_Slate, fg= Yellow_Sulphur)
Track_0_info_Button.config(font=(Font_UI, 7, BOLD))
Track_0_info_Button.place(relx = 0.79, rely = 0.30, anchor = CENTER)

Input_Box_message5 = Label(root, text="Pitch shift:",bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
Input_Box_message5.config(font=(Font_UI, 8, BOLD))
Input_Box_message5.place(relx = 0.87, rely = 0.48, anchor = CENTER)

Input_Box_message6 = Label(root, text="Higher pitch",bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
Input_Box_message6.config(font=(Font_UI, 6, BOLD))
Input_Box_message6.place(relx = 0.87, rely = 0.54, anchor = CENTER)

Input_Box_message6 = Label(root, text="Lower pitch",bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
Input_Box_message6.config(font=(Font_UI, 6, BOLD))
Input_Box_message6.place(relx = 0.87, rely = 0.823, anchor = CENTER)

#Track numbers over.

Input_Box_message5 = Label(root, text="| Track ID |        | Volume |   | Panning |   | Instrument |   | Track Volume |",bg=Dark_Olive_Slate, fg=Yellow_Sulphur)
Input_Box_message5.config(font=(Font_UI, 6, BOLD))
Input_Box_message5.place(relx = 0.05, rely = 0.23, anchor = NW)

#Open file
OpenFile_Button = Button(root, text="Load",bg= Blue_Salvia, fg= Dark_Olive_Slate, command=RawConvertor_fromfile)
OpenFile_Button.place(relx = 0.74, rely = 0.18, anchor = CENTER, width="180")

VolumeEditor_Button = Button(root, text="Volume\nEditor",bg= Blue_Salvia, fg= Dark_Olive_Slate, command=openNew_volume_Window)
VolumeEditor_Button.config(font=(Font_UI, 7, BOLD))
VolumeEditor_Button.place(relx = 0.71, rely = 0.92, anchor = CENTER, width="60", height = "40")

#info_button = Button(root, text="Instrument list.",bg= Blue_Salvia, fg= Dark_Olive_Slate, command= lambda: TK_Message(instrument_List,"Instrument IDs"))
#info_button.place(relx = 0.74, rely = 0.9, anchor = CENTER, width="150")

convert_Button2 = Button(root, state= "disabled", text="Convert",bg= Blue_Salvia, fg= Dark_Olive_Slate)
convert_Button2.place(relx = 0.87, rely = 0.93, anchor = CENTER, width="75")
#Convert file
root.mainloop()

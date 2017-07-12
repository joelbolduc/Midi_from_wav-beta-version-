# Midi_from_wav-beta-version-
Extracts notes from a .wav file, with the ultimate purpose of creating a piano midi file.
This is a beta version. It will eventually be used to generate midi. Currently prints list of all notes played at each point in time (which can easily be turned into midi messages).
the number of samples in a time step, as well as the level of tolerance for discarding noise ; need to be specified when the function is called.
Uses Normalizer, a .py file used in my Audio_Potential project.
To execute, open Note_Extractor il your favorite python editor and execute the script.
Since this is a beta, you will need to manually change the name of the file you want to run it on in the function compress function (fourth-to-last line of code).
Change nothing else, and when you execute the script, you will get a list of notes printed in the (time,(note,intensity)) format.
stereo files will generate an error.

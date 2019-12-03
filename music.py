#!/usr/local/bin/python3
from music21 import *

snpList = [22,58,64,301,393,588,621,669,690]

seg="AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTGGTTACCTGCCGTGAGTAAATTAAAATTTTATTGACTTAGGTCACTAAATACTTTAACCAATATAGGCATAGCGCACAGACAGATAAAAATTACAGAGTACACAACATCCATGAAACGCATTAGCACCACCATTACCACCACCATCACCATTACCACAGGTAACGGTGCGGGCTGACGCGTACAGGAAACACAGAAAAAAGCCCGCACCTGACAGTGCGGGCTTTTTTTTTCGACCAAAGGTAACGAGGTAACAACCATGCGAGTGTTGAAGTTCGGCGGTACATCAGTGGCAAATGCAGAACGTTTTCTGCGTGTTGCCGATATTCTGGAAAGCAATGCCAGGCAGGGGCAGGTGGCCACCGTCCTCTCTGCCCCCGCCAAAATCACCAACCACCTGGTGGCGATGATTGAAAAAACCGGCCAGGATGCTTTACCCAATATCAGCGATGCCGAACGTATTTTTGCCGAACTTTTGACGGGACTCGCCGCCGCCCAGCCGGGGTTCCCGCTGGCGCAATTGAAAACTTTCGTCGATCAGGAATTTGCCCAAATAAAACATGTCCTGCATGGCATTAGTTTGTTGGGGCAGTGCCCGGATAGCATCAACGCTGCGC"

cipher = {
  "AA": "C4",
  "AC":"C4",
  "AG":"D4",
  "AT": "D4",
  "CA": "E-4",
  "CC": "E-4",
  "CG": "F4",
  "CT": "F4",
  "GA": "G4",
  "GC": "G4",
  "GG": "A-4",
  "GT": "A-4",
  "TA": "B-4",
  "TC": "B-4",
  "TG": "C5",
  "TT": "C5"
}
RH = stream.Part()
LH = stream.Part()

s = stream.Score()

def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def mutateCipher(tib):
    for key in cipher.keys():
        if key == tib:
            bleh = note.Note(cipher[tib])
            cipher[key] = bleh.transpose(interval.Interval(1)).nameWithOctave


def pattern2(notes):
    print(notes)
    pattern = [1,2,1,2,3,4,3,4]
    for i in pattern:
        n = note.Note(notes[i - 1]).transpose(interval.Interval(-12))
        n.duration.type = 'eighth'
        LH.append(n)

def pattern1(notes):
    notes = Remove(notes)
    c = chord.Chord(notes).transpose(interval.Interval(-12))
    c.duration.type = 'whole'
    LH.append(c)

##TODO
def pattern3(notes):
    d1 = duration.Duration(quarterLength=1.5)
    d2 = duration.Duration(quarterLength=2.5)
    n1 = note.Note(notes[0]).transpose(interval.Interval(-12))
    n2 = chord.Chord(notes.pop(0)).transpose(interval.Interval(-12))
    n2.duration=d2
    n1.duration=d1
    LH.append(n1)
    LH.append(n2)

basePart = []
j = 0
for i in range(len(seg) - 1):
    ##Go thru the tibbles
    tib = seg[i] + seg[i+1]
    ##build the left hand part based on each measure of the right hand part
    j = j + 1
    basePart.append(cipher[tib])
    if(j == 4):
        if( i < 190):
            pattern1(basePart)
        elif(i >= 190 and i < 255):
            pattern2(basePart)
        elif(i >= 255 and i < 336):
            pattern1(basePart)
        elif(i >= 336):
            pattern2(basePart)
        basePart = []
        j = 0
    ##account for snps
    if i in snpList:
        mutateCipher(tib)
    ##append then increment
    RH.append(note.Note(cipher[tib]))
    i = i + 1


s.insert(0,RH)
s.insert(0,LH)
environment.set('midiPath', '/usr/bin/timidity')
environment.set('musicxmlPath','/usr/bin/musescore')
sg = layout.StaffGroup([RH,LH], symbol='brace')
sg.barTogether = 'Mensurstrich'
s.insert(0, sg)
s.show()

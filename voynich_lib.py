#! /usr/bin/python3

"""
	A library to handle the ascii transcritions of voynich in text16e6.evt

	Notes:
		-There are lots of comments. We ignore them.
		-Lines we care about have a header of the form:
			<f[0-9]{1:3}r.P.[0-9]{1-3};'TRANSCRIPTION_CODE'>
		where 'TRANSCRIPTION_CODE' is substituted for a single letter
		signifying a transcriber. 


"""

def strchr(string, char):
	for i in range(0,len(string)):
		if string[i] == char:
			return i
	return None

def rstrchr(string, char):
	for i in range(len(string),0):
		if string[-i] == char:
			return i
	return None


def get_line_header( line, transcription=None, page=None ):
	begin_i = strchr(line,'<')
	end_i = strchr(line,'>') + 1
	header = line[begin_i:end_i]
	return header

def remove_line_header(line):
	return line.replace(get_line_header(line), "")

def parse_line_header( line, transcription=None, page=None ):
	header = get_line_header(line)
	match_transcriber = False
	page_match = False
	if transcription:
		if header[-2] == transcription:
			match_transcriber = True
	if page:
		split= header.split('.')
		if str(page) == split[-1].split(";")[0]:
				page_match = True
	if not transcription and not page:
		return line
	if transcription and not page and match_transcriber:
		return line
	if not transcription and page and page_match:
		return line
	if transcription and match_transcriber and page and page_match:
		return line
	return None

	

"""
Transcriber codes
# -----------------
#
# [ The following transcriber codes were inherited from INTERLN.EVT: ]
#
#   C: Currier's transcription plus new additions from members of the
#      voynich list as found in the file voynich.now.
#   F: First study group's (Friedman's) transcription including various
#      items as found in the file FSG.NEW.
#   T: John Tiltman's transcription of some pages.
#   L: Don Latham's recent transcription of some pages.
#   R: Mike Roe's recent transcription of some pages.
#   K: Karl Kluge's transcription of some labels from Petersen's copies.
#   J: Jim Reed's transcription of some previously unreadable characters.
#   
# [ The following codes were added by J. Stolfi after 05 Nov 1997,
# in the unfolding of "[|]" groups:
#
#   D: second choice from [|] in "C" lines.
#   G: second choice from [|] in "F" lines, mostly from [1609|16xx].
#   I: second choice from [|] in "J" lines.
#   Q: second choice from [|] in "K" lines.
#   M: second choice from [|] in "L" lines. 
#   
# The following codes were assigned by J. Stolfi for use in 
# "new" transcriptions:
#
#   H: Takeshi Takahashi's full transcription (see f0.K).
#   N: Gabriel Landini.
#   U: Jorge Stolfi.
#   V: John Grove.
#   P: Father Th. Petersen (a few readings reported by K. Kluge).
#   X: Denis V. Mardle.
#   Z: Rene Zandbergen.
# ]

"""

def TRANSCRIBER(name):
	if string_name.contains("Friedman") or string_name.contains("FSG"):
		return "F"
	if string_name.contains("Tiltman"):
		return "T"
	if string_name.contains("Lathams"):
		return "L"
	if string_name.contains("Roe"):
		return "R"
	if string_name.contains("Kluge"):
		return "K"
	if string_name.contains("Reed"):
		return "R"
	if string_name.contains("Takahashi"):
		return 'H'
	if string_name.contains("Landini"):
		return "N"
	if string_name.contains("Stolfi"):
		return "U"
	if string_name.contains("Currier"):
		return "C"
	if string_name.contains("Grove"):
		return "V"
	if string_name.contains("Peterson"):
		return "P"
	if string_name.contains("Mardle"):
		return "X"
	if string_name.contains("Zandbergen"):
		return "Z"



def split_with_selector(line, include_dubious=False):
	final = []
	splat = line.split(".")
	if include_dubious:
		for item in splat:
			for split_item in item.split(","):
				final.append(split_item)
	else:
		for item in splat:
			final.append(item.replace(",",""))
	return final


def remove_comments(line):
	line = line
	while "{" in line:
		begin = strchr(line,"{")
		end = strchr(line,"}")+1
		line = line.replace(line[begin:end],"")
	return line

def remove_filler(line):
	line = line.replace("!","")
	return line.replace("%","")

def remove_breaks(line):
	line=line.replace("=", "")
	line=line.replace("\n","")
	return line.replace("-", "")
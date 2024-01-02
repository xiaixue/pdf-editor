import pypdf as pdf
import tkinter.filedialog as fdlg
import io

def main():

  print(f"""      ___        _____          ___         \n     /  /\      /  /::\        /  /\        \n    /  /::\    /  /:/\:\      /  /:/_       \n   /  /:/\:\  /  /:/  \:\    /  /:/ /\      \n  /  /:/~/:/ /__/:/ \__\:|  /  /:/ /:/      \n /__/:/ /:/  \  \:\ /  /:/ /__/:/ /:/       \n \  \:\/:/    \  \:\  /:/  \  \:\/:/        \n  \  \::/      \  \:\/:/    \  \::/         \n   \  \:\       \  \::/      \  \:\         \n    \  \:\       \__\/        \  \:\        \n     \__\/                     \__\/        \n      ___          _____                                  ___           ___     \n     /  /\        /  /::\       ___           ___        /  /\         /  /\    \n    /  /:/_      /  /:/\:\     /  /\         /  /\      /  /::\       /  /::\   \n   /  /:/ /\    /  /:/  \:\   /  /:/        /  /:/     /  /:/\:\     /  /:/\:\  \n  /  /:/ /:/_  /__/:/ \__\:| /__/::\       /  /:/     /  /:/  \:\   /  /:/~/:/  \n /__/:/ /:/ /\ \  \:\ /  /:/ \__\/\:\__   /  /::\    /__/:/ \__\:\ /__/:/ /:/___\n \  \:\/:/ /:/  \  \:\  /:/     \  \:\/\ /__/:/\:\   \  \:\ /  /:/ \  \:\/:::::/\n  \  \::/ /:/    \  \:\/:/       \__\::/ \__\/  \:\   \  \:\  /:/   \  \::/~~~~ \n   \  \:\/:/      \  \::/        /__/:/       \  \:\   \  \:\/:/     \  \:\     \n    \  \::/        \__\/         \__\/         \__\/    \  \::/       \  \:\    \n     \__\/                                               \__\/         \__\/    \n
  
  """)

  print("""\tChoose what you need: 
                      ( a ) Join .pdf files
                      ( b ) Rotate pages of .pdf file
                      ( c ) Divide a .pdf file in various files\n""")
  while True:
    choose = str(input("""                       Option: """))
    if choose.lower() == "a":
      joiner()
    elif choose.lower() == "b":
      rotator()
    elif choose.lower() == "c":
      separator()
    else:
      continue
      
def joiner():
  
  filenames = file_path_getter(multiple= True)

  print("")
  for i, k in enumerate(filenames):
    fl_name = k.split("/")[-1]
    print(f"                       {i+1}:\t{fl_name}")

  print("\n\tSelect the files in the order you desire (comma separated). Ex: 2,4,1,6\n")
  while True:
    orden = input("\t-> ")
    orden = orden.replace(" ", "")
    orden = orden.replace(".", "")
    orden = orden.replace("-", "")
    orden = orden.split(",")
    indexes = []
    try:
      for i in orden:
        ind = int(i)
        indexes.append(filenames[ind-1])
      break
    except:
      print("Error")
      continue
  
  merger = pdf.PdfWriter()
  for i in indexes:
    merger.append(i)
  
  io_file = io.BytesIO()

  merged_file = merger.write(io_file)
  merger.close()
  merged_file = merged_file[1].getvalue()

  file_path = fdlg.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

  if file_path:
    output_file = open(file_path, "wb")
    output_file.write(merged_file)
    output_file.close()
    print("\n\tSuccess.\n")
    return
  else:
    print("\n\tFailed.\n")
    return

def rotator():
  
  filename = file_path_getter()

  print("")
  reader = pdf.PdfReader(filename)
  writer = pdf.PdfWriter()

  print(f"\n\tChoose the pages to rotate right, if they are all the pages input ALL, if you are done input END. Write them again to rotate them more times.\n\tTotal pages: {len(reader.pages)}. Ex: 2,8,3-5,9\n")

  for i in reader.pages:
    writer.add_page(i)
  
  while True:
    pags = input("\t-> ")
    pags = pags.replace(" ", "")
    pags = pags.replace(".", "")

    if pags.upper() == "ALL":
      for i in writer.pages:
        i.rotate(90)
    elif pags.upper() == "END":
      break
    elif is_int(pags) == True:
      if 0 < int(pags) <= len(writer.pages):
        writer.pages[int(pags)-1].rotate(90)
      else:
        print("Error")
    else:
      pags = pags.split(",")
      for k in pags:
        try:
          if "-" in k:
            pair = k.split("-")
            if len(pair) != 2:
              print("Error")
              break
            elif is_int(pair[0]) == False or is_int(pair[1]) == False:
              print("Error")
              break
            elif pair[0] == pair[1]:
              print("Error")
              break
            elif (0 < int(pair[0]) <= len(writer.pages)) == False or (0 < int(pair[1]) <= len(writer.pages)) == False:
              print("Error")
              break
            else: continue
          else:
            int(k)
        except:
          print("Error")
          break
      else:
        for k in pags:
          if "-" in k:
            pair = k.split("-")
            if int(pair[0]) <= int(pair[1]):
              low_p = int(pair[0])
              hig_p = int(pair[1])
            else: 
              low_p = int(pair[1])
              hig_p = int(pair[0])
            for j in range(low_p, hig_p + 1, 1):
              writer.pages[int(j)-1].rotate(90)
          else:
            writer.pages[int(k)-1].rotate(90)
        continue

  io_file = io.BytesIO()

  rotated_file = writer.write(io_file)
  writer.close()
  rotated_file = rotated_file[1].getvalue()

  file_path = fdlg.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

  if file_path:
    output_file = open(file_path, "wb")
    output_file.write(rotated_file)
    output_file.close()
    print("\n\tSuccess.\n")
    return
  else:
    print("\n\tFailed.\n")
    return

def separator():
  
  filename = file_path_getter()

  print("")
  reader = pdf.PdfReader(filename)
  writer = pdf.PdfWriter()

  print(f"\n\tInput the pages that you desire to extract/divide to a file. If you are done write END. \n\tTotal pages: {len(reader.pages)}. Ex: 2,8,3-5,9\n")

  while True:
    pags = input("\t-> ")
    pags = pags.replace(" ", "")
    pags = pags.replace(".", "")

    checker = True

    """
    Input parsing and error handling
    """
    
    if pags.upper() == "END":
      break
    elif is_int(pags) == True:
      if 0 < int(pags) <= len(reader.pages):
        pass
      else:
        print("Error")
        continue
    else:
      pags_copy = pags.split(",")
      
      for paginas in pags_copy:
        if is_int(paginas) == True:
          if (0 < int(paginas) <= len(reader.pages)) == False:
            print("Error. Pages out of range")
            break
          continue

        paginas = paginas.split("-")

        if len(paginas) != 2:
          print("Error")
          break
        if is_int(paginas[1]) == False or is_int(paginas[0]) == False:
          print("Error")
          break
        if not 0 < int(paginas[0]) <= len(reader.pages):
          print("Error")
          break
        if not 0 < int(paginas[1]) <= len(reader.pages):
          print("Error")
          break
      else:
        checker = False

    if checker == True:
      continue

    """
    Pages processing
    """
    for j in pags.split(","):
      if is_int(j) == True:
        writer.add_page(reader.pages[ int(j) - 1 ])
      else:
        j = j.split("-")

        if int(j[0]) < int(j[1]):
          for k in range( int(j[0]) - 1, int(j[1]), 1):
            writer.add_page(reader.pages[ int(k) ])
        else:
          for k in range(int(j[1]) - 1, int(j[0]), 1):
            writer.add_page(reader.pages[ int(k) ])
    
    while True:
      io_file = io.BytesIO()

      rotated_file = writer.write(io_file)
      writer.close()
      rotated_file = rotated_file[1].getvalue()

      file_path = fdlg.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

      if file_path:
        output_file = open(file_path, "wb")
        output_file.write(rotated_file)
        output_file.close()
        print("\n\tSuccess.\n")
      else:
        print("\n\tFailed.\n")

      print(f"\n\tInput the pages that you desire to extract/divide to a file. If you are done write END. \n\tTotal pages: {len(reader.pages)}\n")
      break
  return

def file_path_getter(multiple= False):
  if multiple == True:
    while True:
      file_path_string = fdlg.askopenfilenames(
            title='Select which files you want to join',
            initialdir='/',
            filetypes=(('pdf files', '*.pdf'), ('All files', '*.*')))
      
      if file_path_string == "":
        continue
      else:
        return file_path_string
  else:
    while True:
      file_path_string = fdlg.askopenfilename(
        title='Select file',
        initialdir='/',
        filetypes=(('pdf files', '*.pdf'), ('All files', '*.*')))
      
      if file_path_string == "" or file_path_string[-3::] != "pdf":
        continue
      else:
        return file_path_string

def is_int(num):
  try:
    int(num)
    return True
  except:
    return False

if "__main__" == __name__:
  main()
  
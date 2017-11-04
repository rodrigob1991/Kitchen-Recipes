from tkinter import *
from tkinter import messagebox

def abrir_archivo(f):
      def deco(*args):
            with open("data.recp", "r") as file:
                  return f(file, *args)
      return deco

def openWriteFile(f):
      def decowrite(*args):
            with open("data.recp", "r+") as file:
                  return f(file, *args)
      return decowrite

@openWriteFile
def write_file(file,ingredients,description_recipe):
    content=file.read()
    final_file=file.tell()
    file.write(ingredients+"\n"+description_recipe)
 

@abrir_archivo
def pasar_ing (file):


      #file = open("data.recp", "r")
      receta=[]
      listIng=[]
      flag = "ing" #ing or rec

      for line in file.readlines():
            if flag != "ing":
                  flag = "ing"
            else:
                  things = line.split(",")
                  for ing in things:
                        if ing not in listIng and ing != "\n":
                              listIng.append(ing)
                  flag = "rec"


      #file.close()

      return listIng

@abrir_archivo
def busc_recetas(file, searchlist):

      typeflag = "ing"
      savenext = False
      #searchResult = "No matches found."
      searchResult = []
      sortedList  = []
      results = 0
      index = 0

      #file_recetas = open("recetas.txt", "r")

      for line in file.readlines():
            line = line.strip()
            #no tengo que cuestionarme
            if savenext == True:
                  print(line)
                  searchResult.append("")
                  searchResult[results] = [line, index]
                  results += 1
                  savenext = False
                  typeflag = "ing"
            else:
                  if typeflag == "ing":
                        typeflag = "rec"
                        things = line.split(",")

                        match = 0
                        for ingredientIhave in searchlist:
                              for ingredientIneed in things:

                                    if ingredientIhave == ingredientIneed:
                                          match +=1

                        #print(match)

                        if match >= 1:
                              savenext = True
                              total = len(line.split(",")) - 1
                              index = total - match
                              negativeIndex = len(searchlist) - match
                              index = index + negativeIndex

                              print(index)


                  elif typeflag == "rec":
                        typeflag = "ing"

      if results == 0:
            sortedList.append("No se encontraron recetas que cumplan con los parametros")
      else:
            searchResult = sorted(searchResult, key=lambda item: item[1])

            #for i, res in enumerate(searchResult):
            #    sortedList.append(searchResult[i][0])

            #for elemento in searchResult:
            #    sortedList.append(elemento[0])

            #for a, b in searchResult:
            #    sortedList.append(a)

            sortedList = [elemento[0] for elemento in searchResult]
            #sortedList = [a for a, b in searchResult]

            print(sortedList)

      return sortedList




class ventana1:
            def __init__(self, master):

                        
                        self.master = master
                        self.master.geometry("200x500")
                        self.master.config(bg="blue")
                        self.checkList =[]
                        self.ingList=pasar_ing()
                        Label(self.master,text="SELECCIONAR INGREDIENTES").place(x=10,y=20)
                        self.list_box_ing=Listbox(self.master,selectmode=MULTIPLE)
                        self.list_box_ing.insert(0,*self.ingList)
                        self.list_box_ing.place(x=10,y=50)

                        Button(self.master,text="BUSCAR",command=self.selec_ing).place(x=20,y=300)
                        Button(self.master,text="CERRAR",bg="red",command=self.closewindow).place(x=100,y=300)


            def selec_ing(self):

                        searchlist = []

                        for indice in (self.list_box_ing.curselection()):
                              searchlist.append(self.ingList[indice])
                              
                       
                        if  searchlist==[]:
                                          
                              messagebox.showwarning("Advertencia","No seleccionaste ningun ingrediente")
                                
                        else:         
                                                             
                              searchResult=busc_recetas(searchlist)
                              window22 = Toplevel(root)
                              gui22 = win_result(window22, searchlist,searchResult)

            def closewindow(self):
                        self.master.destroy()


class ventanaPrincipal:
            def __init__(self, master):

                        self.master = master
                        frame = Frame(self.master, width=700, height=200)
                        frame.config(bg="blue")
                        frame.pack()
                        Label(frame,text="PROGRAMA DE RECETAS",font="Helvetica 30 bold italic").place(x=90,y=40)
                        Button(frame,text="BUSCAR RECETAS",bg="white",font="Helvetica 15 bold italic",command=self.search).place(x=300,y=150)
                        Button(frame,text="SALIR",bg="red",font="Helvetica 15 bold italic",command=self.quitApp).place(x=550,y=150)
                        Button(frame,text="CREAR RECETA",bg="white",font="Helvetica 15 bold italic",command=self.newRecipe).place(x=50,y=150)

            def quitApp(self):
                        self.frame.destroy()

            def search(self):
                        window2 = Toplevel(root)
                        gui2 = ventana1(window2)

            def newRecipe(self):
                        window3 = Toplevel(root)
                        gui3 = WinCreateRecipe(window3)


class win_result:

    def __init__(self, master, searching,searchResult):

            def order_result():
                
                index=1
                line_size=0
                recipe_all_order=""
                recipe_all_order=str(index)+recipe_all_order
                for result in searchResult:
                    for character in result:

                            if line_size==40:
                                recipe_all_order=recipe_all_order+character+"\n"
                                line_size=0
                                
                            else:
                                recipe_all_order=recipe_all_order+character
                                line_size=line_size+1
                    index=index+1
                    line_size=0            
                    recipe_all_order=recipe_all_order+"\n"+str(index)+"-"
                    
                recipe_all_order=recipe_all_order.rstrip(str(index)+"-"+"\n")   
                return recipe_all_order
                                    
            self.title="Resultados de la búsqueda"
            self.master = master
            self.master.config(bg="black")
            self.master.geometry("700x500")
            Label(master, text="RESULTADOS DE LA BUSQUEDA",font="Arial 27 bold italic").place(x=50,y=30)  
            Label(master, text=order_result(),justify="left",bg="yellow",font="Helvetica 15 bold italic").place(x=135,y=110)
            Button(master,text="CERRAR",bg="red",font="Helvetica 15 bold italic",command=self.exit).place(x=10,y=400)

    def exit(self):
        self.master.destroy()

class WinCreateRecipe:

    def __init__(self,master):

        self.master=master
        self.master.geometry("700x300")
        self.recipe_description=StringVar()
        self.ingredients=StringVar()
        Label(self.master,text="Ingresar ingredientes",font="Arial 13 bold italic").place(x=20,y=30)
        Entry(self.master,width=80,textvariable=self.ingredients).place(x=20,y=60)
        Label(self.master,text="Ingresar descripcion de receta",font="Arial 13 bold italic").place(x=20,y=100)
        Entry(self.master,width=110,textvariable=self.recipe_description).place(x=20,y=140)
        Label(self.master,text="!Separar ingredientes por coma¡",font="Arial 15 bold italic",bg="white").place(x=20,y=0)
        Button(self.master,text="CREAR RECETA",font="Arial 20 bold italic",bg="blue",command=self.create).place(x=20,y=200)
        Button(self.master,text="SALIR",font="Arial 20 bold italic",bg="red",command=self.close).place(x=350,y=200)
        

    def create(self):

        format_Ing=","
        entry_ings=self.ingredients.get()
        entry_ings=entry_ings.strip(" ")
        entry_ings=entry_ings+","

        for character in entry_ings:
            
            if character.isalnum()==True or character==",":
                format_Ing=format_Ing+character
            

            if format_Ing[len(format_Ing)-2]==","and character==",":
                format_Ing=format_Ing[:len(format_Ing)-1]
                    
        format_Ing=format_Ing.lower()
        format_Ing=format_Ing.lstrip(",")

        format_recipe=self.recipe_description.get()
        format_recipe=format_recipe.strip(" ")
        format_recipe=format_recipe.strip(".")
        format_recipe=format_recipe+"."

        if format_recipe=="." or format_Ing=="":
            messagebox.showwarning("Advertencia","No escribiste ingredientes o recetas")
        else:
            write_file(format_Ing,format_recipe)

    def close(self):

        self.master.destroy()

root = Tk()
gui1 = ventanaPrincipal(root)
root.mainloop()

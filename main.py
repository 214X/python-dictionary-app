import dictFunctions as df

def printMenu():
    print("\n" + "=" * 50)
    print("         ENGLISH DICTIONARY MANAGER")
    print("=" * 50)
    print("1. Create Dictionary")
    print("2. Load Dictionary")
    print("3. Save Dictionary")
    print("4. Remove Dictionary")
    print("5. Dictionary Information")
    print("6. Add Word")
    print("7. Remove Word")
    print("8. Search Word")
    print("9. List Words")
    print("0. Exit")
    print("=" * 50)

def main():
    run_flag = True

    while run_flag:
        printMenu()
        menuChoice = input("Select an option (1-9) > ").strip()
        print("\n")
        
        try:
            match menuChoice:
                # -----(1)(CREATE DICTIONARY)----------------------------------------------
                case "1":
                    print("Create Dictionary")
                    print("-----------------")
                    name = input("Enter a name for the new dictionary > ").strip()
                    path = input("Enter a path for the new dictionary > ").strip()

                    if path == "":
                        path = "." # consider current path as default

                    df.createDict(name, path)
                    print("Dictionary created successfully.")

                # -----(2)(LOAD DICTIONARY)------------------------------------------------
                case "2":
                    print("Load Dictionary")
                    print("----------------")
                    name = input("Dictionary name > ").strip()
                    path = input("Dictionary path > ").strip()

                    if path == "":
                        path = "."

                    df.loadDict(name, path)
                    print("Dictionary loaded successfully.")

                # -----(3)(SAVE DICTIONARY)------------------------------------------------
                case "3":
                    print("Save Dictionary")
                    print("----------------")
                    name = input("Dictionary name > ").strip()
                    path = input("Dictionary path > ").strip()

                    if path == "":
                        path = "."

                    df.saveDict(name, path)

                # -----(4)(REMOVE DICTIONARY)----------------------------------------------
                case "4":
                    print("Remove Dictionary")
                    print("-----------------")
                    name = input("Dictionary name > ").strip()
                    path = input("Dictionary path > ").strip()

                    if path == "":
                        path = "."

                    df.removeDict(name, path)
                    print("Dictionary removed successfully.")

                # -----(5)(DICTIONARY INFORMATION)-----------------------------------------
                case "5":
                    print("Dictionary Information")
                    print("----------------------")
                    name = input("Dictionary name > ").strip()
                    path = input("Dictionary path > ").strip()

                    if path == "":
                        path = "."

                    df.dictInfo(name, path, showResult=True)

                # -----(6)(ADD WORD)-------------------------------------------------------
                case "6":
                    print("Add Word")
                    print("--------")

                    word = input("Word > ").strip()

                    # show menu for valid PoS
                    print("Part of Speech\n",
                        "1. adjective\n",
                        "2. adverb\n",
                        "3. noun\n",
                        "4. verb")
                    
                    pos_choice = input("Select (1-4) > ").strip()

                    match pos_choice:
                        case "1":
                            pos = "adjective"
                        case "2":
                            pos = "adverb"
                        case "3":
                            pos = "noun"
                        case "4":
                            pos = "verb"
                        case _:
                            raise ValueError("Invalid part of speech.")

                    plural = input(
                        "Plural (leave empty for automatic) > "
                    ).strip()

                    if plural == "": #if plural is empty consider it as "Default"
                        plural = "Default"

                    definitions = []

                    print("Enter definitions.")
                    print("Press ENTER on an empty line to finish.")
                    while True:
                        definition = input(
                            f"Definition {len(definitions) + 1} > "
                        ).strip()

                        if definition == "":
                            break # end the definition enterence

                        definitions.append(definition)

                    df.addWord(
                        word,
                        pos,
                        *definitions,
                        plural=plural
                    )

                    print("Word added successfully.")

                # -----(7)(REMOVE WORD)----------------------------------------------------
                case "7":
                    print("Remove Word")
                    print("-----------")
                    word = input("Word > ").strip()
                    if df.searchWord(word) is None:
                        print("Word not found.")
                    else:
                        df.removeWord(word)
                        print("Word removed successfully.")

                # -----(8)(SEARCH WORD)----------------------------------------------------
                case "8":
                    print("Search Word")
                    print("-----------")
                    word = input("Word > ").strip()

                    df.searchWord(
                            word,
                            showResult=True
                        )

                # -----(9)(LIST WORDs)-----------------------------------------------------
                case "9":
                    print("List Words")
                    print("----------")
                    df.listWords(showResult=True)

                # -----(0)(EXIT)-----------------------------------------------------------
                case "0":
                    print("Goodbye!")
                    run_flag = False

                # -----(ELSE)(INVALID CHOICE)----------------------------------------------
                case _:
                    print("Invalid option. Please try again.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
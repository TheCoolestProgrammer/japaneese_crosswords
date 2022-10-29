from windows_system import Menu,Window
def create_menu(screen_width):
    menu_width = 100
    menu_height = 20

    menu = Menu(screen_width, 20, 0, 0)
    menu.isactive=True

    file_menu = Menu(menu_width, menu_height, 0, 0, "file")
    field_menu = Menu(menu_width, menu_height, menu_width, 0, "field")
    menu.submenu.append(file_menu)
    menu.submenu.append(field_menu)

    save_menu = Menu(menu_width, menu_height, 0, menu_height, "save")
    file_menu.submenu.append(save_menu)

    save_window = Window("save as")
    save_window = save_window.create_window_ok("save")

    save_menu.link.append(save_window)
    # block2
    rows_menu = Menu(menu_width, menu_height, menu_width, menu_height, "rows")
    columns_menu = Menu(menu_width, menu_height, menu_width, menu_height * 2, "columns")
    clear_menu = Menu(menu_width, menu_height, menu_width, menu_height * 3, "clear")
    field_menu.submenu.append(rows_menu)
    field_menu.submenu.append(columns_menu)
    field_menu.submenu.append(clear_menu)

    rows_window = Window()
    rows_window = rows_window.create_window_slider("rows")
    columns_window = Window()
    columns_window = columns_window.create_window_slider("columns")
    clear_window = Window()
    clear_window = clear_window.create_window_ok("clear")

    rows_menu.link.append(rows_window)
    columns_menu.link.append(columns_window)
    clear_menu.link.append(clear_window)

    return [menu,file_menu,save_menu,field_menu, rows_menu,columns_menu,clear_menu]
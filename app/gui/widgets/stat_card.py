
import customtkinter as ctk


class StatCard(ctk.CTkFrame):

    def __init__(
        self,
        master,
        title,
        value,
        icon,
        accent="#2563EB"
    ):

        super().__init__(

            master,

            fg_color="#202938",

            corner_radius=18,

            border_width=2,

            border_color=accent,

            width=260,

            height=145

        )

        self.grid_propagate(False)

        # ==========================
        # Icon
        # ==========================

        icon_label = ctk.CTkLabel(

            self,

            text=icon,

            font=("Segoe UI Emoji", 30)

        )

        icon_label.pack(

            anchor="w",

            padx=20,

            pady=(18,5)

        )

        # ==========================
        # Value
        # ==========================

        value_label = ctk.CTkLabel(

            self,

            text=value,

            font=("Segoe UI",30,"bold"),

            text_color="white"

        )

        value_label.pack(

            anchor="w",

            padx=20

        )

        # ==========================
        # Title
        # ==========================

        title_label = ctk.CTkLabel(

            self,

            text=title,

            font=("Segoe UI",15),

            text_color="#94A3B8"

        )

        title_label.pack(

            anchor="w",

            padx=20,

            pady=(2,15)

        )
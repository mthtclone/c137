class DialogTrigger:
    def __init__(self, player, dialog_manager, metadata):
        self.player = player

        self.dialog_manager = dialog_manager

        self.metadata = metadata

        self.triggered_planes = set()

        self.dialogs = {
            "COL_Plane1": "DT0",
            "COL_Road": "DT1",
            "COL_Plane2": "DT2",
            "COL_Plane3": "DTall",
        }

    def update(self):
        current_plane = self.player.ground_detector.last_surface

        if current_plane is None:
            return

        if current_plane in self.dialogs:
            if current_plane not in self.triggered_planes:
                self.dialog_manager.start(self.dialogs[current_plane])

                self.triggered_planes.add(current_plane)

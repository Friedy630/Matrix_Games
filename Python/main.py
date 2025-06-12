import tetris


async def tetris_main():
    print("Starting Tetris...")
    tetris.start_tetris()


async def main():
    tetris_main()
    print("let's a go!")


if __name__ == "__main__":
    main()


"""

diff1_step_interval_seconds = 1.0
diff2_step_interval_seconds = 0.75
diff3_step_interval_seconds = 0.5

# Shapes for menu
close_x_shape = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
space_shape = np.array([[1, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1]])
space_shape = gl.get_rotated_shape_matrix(space_shape, True)
s_shape = np.array([[1, 1], [1, 0], [1, 1], [0, 1], [1, 1]]).T
p_shape = np.array([[1, 1], [1, 1], [1, 1], [1, 0], [1, 0]]).T
e_shape = np.array([[1, 1], [1, 0], [1, 1], [1, 0], [1, 1]]).T
d_shape = np.array([[1, 0], [1, 1], [1, 1], [1, 1], [1, 0]]).T

progress_bar_border_shape = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
).T

progress_bar_inner_green_shape = np.array([[1, 1, 1], [1, 1, 1]]).T
progress_bar_inner_yellow_shape = np.array([[1, 1, 1, 1], [1, 1, 1, 1]]).T
progress_bar_inner_red_shape = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]).T


def start_main_menu():
    global running, fall_step_interval_seconds
    print("entered main menu")
    fall_step_interval_seconds = diff1_step_interval_seconds
    gl.fill(gl.colors["black"])
    gl.set_shape(progress_bar_border_shape, gl.Vec(1, 1), gl.colors["grey"])
    gl.set_shape(progress_bar_inner_green_shape, gl.Vec(2, 2), gl.colors["green"])
    text_height = 6
    text_color = gl.colors["grey"]
    gl.set_shape(s_shape, gl.Vec(1, text_height), text_color)
    gl.set_shape(p_shape, gl.Vec(4, text_height), text_color)
    gl.set_shape(e_shape, gl.Vec(7, text_height), text_color)
    gl.set_shape(e_shape, gl.Vec(10, text_height), text_color)
    gl.set_shape(d_shape, gl.Vec(13, text_height), text_color)
    gl.show()
    while running:
        if il.inputs["escape"]:
            running = False
        if il.inputs["space"]:
            return True
        if il.inputs["exit"]:
            running = False
            return False
        if fall_step_interval_seconds == diff1_step_interval_seconds:
            if il.inputs["right"]:
                gl.set_shape(
                    progress_bar_inner_yellow_shape, gl.Vec(5, 2), gl.colors["yellow"]
                )
                gl.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff2_step_interval_seconds
        if fall_step_interval_seconds == diff2_step_interval_seconds:
            if il.inputs["right"]:
                gl.set_shape(
                    progress_bar_inner_red_shape, gl.Vec(9, 2), gl.colors["red"]
                )
                gl.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff3_step_interval_seconds
            if il.inputs["left"]:
                gl.set_shape(
                    progress_bar_inner_yellow_shape, gl.Vec(5, 2), gl.colors["black"]
                )
                gl.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff1_step_interval_seconds
        if fall_step_interval_seconds == diff3_step_interval_seconds:
            if il.inputs["left"]:
                gl.set_shape(
                    progress_bar_inner_red_shape, gl.Vec(9, 2), gl.colors["black"]
                )
                gl.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff2_step_interval_seconds
        il.reset_inputs()
        time.sleep(0.1)
    return False

"""

@staticmethod
def sort(values):
    output = ""
    max_len = int(len(values) / 10)
    for value in range(len(values)):
        if value + 1 > 10:
            break

        fade_intensity = int(255 - (value / len(values)) * 255)
        fade_intensity = max(0, min(fade_intensity, 255))

        color_start = f"\033[38;2;255;{fade_intensity};0m"
        color_end = "\033[0m"

        string_out = f"{color_start}{value+1:2d}. {values[value]:<10}{color_end}"
        current_range = value
        for i in range(max_len):
            current_range += 9
            if current_range < len(values):
                fade_intensity = int(255 - ((current_range + i + 1) / len(values)) * 255)
                fade_intensity = max(0, min(fade_intensity, 255))
                color_start = f"\033[38;2;255;{fade_intensity};0m"
                string_out += f"{color_start}{current_range + 1:5d}. {values[current_range]:<10}{color_end}"

        output += string_out + "\n" 
    return output
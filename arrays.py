class Arrays:

    NOTE_NAMES = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']
    #              0    1     2    3     4    5    6     7    8     9    10   11

    NOTE_NAMES_EN = ['C', 'C sharp', 'D', 'D sharp', 'E', 'F', 'F sharp', 'G', 'G sharp', 'A', 'A sharp', 'B']

    OCTAVE_NAMES = ['sub-contra octave', 'contra octave', 'great octave',
                    'small octave', '1-line octave', '2-line octave',
                    '3-line octave', '4-line octave', '5-line octave']

    TUNINGS = [{"Standard": [[3, 4], [3, 9], [4, 2], [4, 7], [4, 11], [5, 4]],      # Guitar
                "Drop D":   [[3, 2], [3, 9], [4, 2], [4, 7], [4, 11], [5, 4]],
                "Custom": [[3, 4], [3, 9], [4, 2], [4, 7], [4, 11], [5, 4]]},
               {"Standard": [[2, 4], [2, 9], [3, 2], [3, 7]],                       # Bass
                "Drop D":   [[2, 2], [2, 9], [3, 2], [3, 7]],
                "Custom": [[2, 4], [2, 9], [3, 2], [3, 7]]},
               {"Standard": [[5, 7], [5, 0], [5, 4], [5, 9]],                       # Ukulele
                "Custom": [[5, 7], [5, 0], [5, 4], [5, 9]]}]

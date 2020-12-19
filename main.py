import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui
import threading

import audio_engine as aeng
from arrays import Arrays
import mainform
import settings


class MainWindow(QMainWindow, mainform.Ui_MainWindow):
    instrument = 0
    notes_array = []
    btns_up_array = []
    btns_down_array = []
    btns_play_array = []
    current_tune = []
    current_note = (3, 4)
    current_note_midi = 64
    frequency_thread = threading.Thread()
    test_mode = False

    def note_arrays_init(self):

        self.notes_array.append(self.textNote1)
        self.notes_array.append(self.textNote2)
        self.notes_array.append(self.textNote3)
        self.notes_array.append(self.textNote4)
        self.notes_array.append(self.textNote5)
        self.notes_array.append(self.textNote6)

        self.btns_down_array.append(self.btnNote1Down)
        self.btns_down_array.append(self.btnNote2Down)
        self.btns_down_array.append(self.btnNote3Down)
        self.btns_down_array.append(self.btnNote4Down)
        self.btns_down_array.append(self.btnNote5Down)
        self.btns_down_array.append(self.btnNote6Down)

        self.btns_up_array.append(self.btnNote1Up)
        self.btns_up_array.append(self.btnNote2Up)
        self.btns_up_array.append(self.btnNote3Up)
        self.btns_up_array.append(self.btnNote4Up)
        self.btns_up_array.append(self.btnNote5Up)
        self.btns_up_array.append(self.btnNote6Up)

        self.btns_play_array.append(self.btnNote1Play)
        self.btns_play_array.append(self.btnNote2Play)
        self.btns_play_array.append(self.btnNote3Play)
        self.btns_play_array.append(self.btnNote4Play)
        self.btns_play_array.append(self.btnNote5Play)
        self.btns_play_array.append(self.btnNote6Play)

    def form_initialisation(self):

        self.note_arrays_init()
        self.set_instrument()

        self.horizontalSlider.setVisible(False)
        self.horizontalSlider.valueChanged.connect(self.slider)

        self.testModeBtn.clicked.connect(self.show_slider)
        self.startTuneBtn.clicked.connect(self.start_stream)
        self.stopTuneBtn.clicked.connect(self.stop_stream)
        self.btnSettings.clicked.connect(self.open_settings)
        self.tuningSelectList.activated[str].connect(self.show_tuning_from_list)
        self.gtrRadioBtn.clicked.connect(self.set_instrument)
        self.bassRadioBtn.clicked.connect(self.set_instrument)
        self.ukeRadioBtn.clicked.connect(self.set_instrument)

        for btn in self.btns_up_array:
            btn.clicked.connect(self.switch_note)
            btn.clicked.connect(self.play_note)
            btn.clicked.connect(self.set_tune_note)

        for btn in self.btns_down_array:
            btn.clicked.connect(self.switch_note)
            btn.clicked.connect(self.play_note)
            btn.clicked.connect(self.set_tune_note)

        for btn in self.btns_play_array:
            btn.clicked.connect(self.play_note)
            btn.clicked.connect(self.set_tune_note)

        aeng.TUNE_NOTE_NUM = [note[1] + (note[0] + 1) * 12 for note in self.current_tune]
        aeng.TUNE_FREQ = [aeng.number_to_freq(num) for num in aeng.TUNE_NOTE_NUM]

        global frequency_thread
        frequency_thread = threading.Thread(target=self.frequency_detect, daemon=True)

    def show_tuning_from_list(self):
        self.current_tune.clear()
        self.current_tune.extend(Arrays.TUNINGS[self.instrument][self.tuningSelectList.currentText()])

        for i in range(len(self.current_tune), 6):
            self.notes_array[i].setEnabled(False)
            self.notes_array[i].setPlainText('')
            self.btns_up_array[i].setEnabled(False)
            self.btns_down_array[i].setEnabled(False)
            self.btns_play_array[i].setEnabled(False)

        for i in range(len(self.current_tune)):
            self.notes_array[i].setEnabled(True)
            self.btns_up_array[i].setEnabled(True)
            self.btns_down_array[i].setEnabled(True)
            self.btns_play_array[i].setEnabled(True)
            self.notes_array[i].setPlainText(Arrays.NOTE_NAMES[self.current_tune[i][1]])
            self.notes_array[i].setToolTip(
                Arrays.NOTE_NAMES_EN[self.current_tune[i][1]] + ", " + Arrays.OCTAVE_NAMES[self.current_tune[i][0]]
            )
        self.current_note = (self.current_tune[0][0], self.current_tune[0][1])
        self.set_tune_note(1)

    def show_tuning_from_btns(self):
        for i in range(len(self.current_tune)):
            self.notes_array[i].setPlainText(Arrays.NOTE_NAMES[self.current_tune[i][1]])
            self.notes_array[i].setToolTip(
                Arrays.NOTE_NAMES_EN[self.current_tune[i][1]] + ", " + Arrays.OCTAVE_NAMES[self.current_tune[i][0]]
            )

    def set_instrument(self):
        if self.sender():
            sender = self.sender().objectName()
        else:
            sender = "None"

        if sender == "gtrRadioBtn":
            self.instrument = 0
        elif sender == "bassRadioBtn":
            self.instrument = 1
        elif sender == "ukeRadioBtn":
            self.instrument = 2
        else:
            self.instrument = 0
        self.tuningSelectList.clear()
        self.tuningSelectList.addItems(Arrays.TUNINGS[self.instrument].keys())
        self.tuningSelectList.setCurrentIndex(0)
        self.show_tuning_from_list()

    def switch_note(self):
        self.tuningSelectList.setCurrentText('Custom')
        self.show_tuning_from_list()

        num = int(self.sender().objectName()[7:8]) - 1
        if self.sender().text() == "+":
            sign = 1
        elif self.sender().text() == "-":
            sign = -1
        else:
            sign = 0
        self.current_tune[num][1] += sign
        if self.current_tune[num][1] < 0:
            self.current_tune[num][0] -= 1
            self.current_tune[num][1] = 11
        if self.current_tune[num][1] > 11:
            self.current_tune[num][0] += 1
            self.current_tune[num][1] = 0
        if self.current_tune[num][0] < 0:
            self.current_tune[num][0] = 0
            self.current_tune[num][1] = 0
            QMessageBox.about(self, 'Warning', 'It\'s time to stop!')
        if self.current_tune[num][0] == 8 and self.current_tune[num][1] > 3:
            self.current_tune[num][0] = 8
            self.current_tune[num][1] = 3
            QMessageBox.about(self, 'Warning', 'It\'s time to stop!')
        self.current_note = self.current_tune[num]
        self.show_tuning_from_btns()

    def play_note(self):
        num = int(self.sender().objectName()[7:8]) - 1
        self.current_note = (self.current_tune[num][0], self.current_tune[num][1])
        path = 'notes/' + str(self.current_note[0]) + '_' + str(self.current_note[1]) + '.ogg'
        aeng.play_note(path)

    def set_tune_note(self, num):
        if num == 0:
            num = int(self.sender().objectName()[7:8])
        self.current_note_midi = (self.current_note[0] + 1) * 12 + self.current_note[1]
        aeng.set_tune_note(self.current_note_midi)
        self.currentNoteLabel.setText(str(Arrays.NOTE_NAMES[self.current_note[1]] + str(self.current_note[0])))
        for x in self.btns_play_array:
            x.setStyleSheet('')
        self.btns_play_array[num - 1]. \
            setStyleSheet('QPushButton{background-color: #0f0;}')

    def start_stream(self):
        aeng.sd_stream_start()
        aeng.sd.wait()
        frequency_thread.start()
        self.statusbar.showMessage('Tuner is on')

    def stop_stream(self):
        if frequency_thread.is_alive():
            self.statusbar.setStatusTip('Tuner is off')
            frequency_thread.join()

    def open_settings(self):
        sets = SettingsWindow(self)
        sets.show()

    def frequency_detect(self):
        while True:
            frequency_now = aeng.frequency()
            self.display_frequency(frequency_now)
            self.statusbar.showMessage(str('Tuner is on. Current freq: ' + (str(frequency_now))))

    def display_frequency(self, frequency_now):

        # detect nearest or selected tuning freq
        selected_freq = aeng.number_to_freq(self.current_note_midi)

        # detect neighbour frequencies
        left, right = aeng.number_to_freq(self.current_note_midi - 1), aeng.number_to_freq(self.current_note_midi + 1)

        if frequency_now != 0:
            difference = frequency_now - selected_freq
            if difference <= 0:
                difference = abs(difference)
                tunebar_left_value = int((min(selected_freq - left, difference) / (selected_freq - left) * 95) + 5)
                tunebar_right_value = 5
            else:
                tunebar_left_value = 5
                tunebar_right_value = int((min(right - selected_freq, difference) / (right - selected_freq) * 95) + 5)
            self.tuneBarLeft.setValue(tunebar_left_value)
            self.tuneBarRight.setValue(tunebar_right_value)
            self.tune_change_color()
        else:
            self.tuneBarLeft.setValue(self.tuneBarLeft.minimum())
            self.tuneBarRight.setValue(self.tuneBarRight.minimum())

    def show_slider(self):
        self.test_mode = not self.test_mode
        self.horizontalSlider.setVisible(self.test_mode)
        if self.test_mode:
            self.testModeBtn.setText('Test mode: ON')
        else:
            self.testModeBtn.setText('Test mode: OFF')

    def slider(self):
        self.display_frequency(self.horizontalSlider.value())
        self.statusbar.showMessage(str('Tuner is on. Current freq: ' + (str(self.horizontalSlider.value()))))

    stylesheet_l = 'QProgressBar { \n  border: 1px solid white; \n  border-right: none;}'
    stylesheet_r = 'QProgressBar { \n  border: 1px solid white; \n  border-left: none;}'

    def tune_change_color(self):
        percentage = max(self.tuneBarLeft.value() * self.tuneBarLeft.maximum() / 100,
                         self.tuneBarRight.value() * self.tuneBarRight.maximum() / 100)
        if percentage <= 15.0:
            add = 'QProgressBar::chunk{ \n  background: green;}\n'
        elif percentage <= 50.0:
            add = 'QProgressBar::chunk{ \n  background: orange;}\n'
        else:
            add = 'QProgressBar::chunk{ \n  background: red;}\n'
        self.tuneBarLeft.setStyleSheet(str(self.stylesheet_l + add))
        self.tuneBarRight.setStyleSheet(str(self.stylesheet_r + add))

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.form_initialisation()


class SettingsWindow(QMainWindow, settings.Ui_MainWindow):
    devices = aeng.sd.query_devices()
    audio_input_array = []
    audio_output_array = []
    sensibility = aeng.SENSIBILITY

    def form_initialisation(self):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        for dev in self.devices:
            if dev["max_input_channels"] > 0:
                self.audio_input_array.append(dev)
                self.audioInputList.addItem(dev["name"])
            if dev["max_output_channels"] > 0:
                self.audio_output_array.append(dev)
                self.audioOutputList.addItem(dev["name"])

        self.audioInputList.setCurrentText(self.devices[aeng.sd.default.device[0]]['name'])
        self.audioOutputList.setCurrentText(self.devices[aeng.sd.default.device[1]]['name'])

        self.btnOk.clicked.connect(self.change_ok)
        self.btnCancel.clicked.connect(self.change_cancel)

        self.sensibilitySlider.setValue(aeng.SENSIBILITY)
        self.sensibilitySlider.sliderMoved.connect(self.sensibility_change)
        self.sensibilitySlider.valueChanged.connect(self.sensibility_change)
        self.senseResetBtn.clicked.connect(self.sensibility_reset)

        self.label_sense.setText(str(aeng.SENSIBILITY))

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key_Escape:
            self.change_cancel()
        elif a0.key() == QtCore.Qt.Key_Enter or a0.key() == QtCore.Qt.Key_Return:
            self.change_ok()
        a0.accept()
        return a0

    def change_input(self):
        for i in range(len(self.devices)):
            if self.devices[i]["name"] == self.audioInputList.currentText():
                aeng.sd.default.device = i, aeng.sd.default.device[1]
                aeng.sd.default.channels = self.devices[i]["max_input_channels"], aeng.sd.default.channels[0],

    def change_output(self):
        for i in range(len(self.devices)):
            if self.devices[i]["name"] == self.audioOutputList.currentText():
                aeng.sd.default.device = aeng.sd.default.device[0], i
                aeng.sd.default.channels = aeng.sd.default.channels[0], self.devices[i]["max_output_channels"]

    def change_ok(self):
        self.change_input()
        self.change_output()
        self.sensibility_set()
        self.close()

    def change_cancel(self):
        self.audioInputList.setCurrentText(self.devices[aeng.sd.default.device[0]]['name'])
        self.audioOutputList.setCurrentText(self.devices[aeng.sd.default.device[1]]['name'])
        self.label_sense.setText(str(self.sensibility))
        self.close()

    def sensibility_change(self):
        self.label_sense.setText(str(self.sensibilitySlider.value()))

    def sensibility_set(self):
        self.sensibility = self.sensibilitySlider.value()
        aeng.SENSIBILITY = self.sensibility

    def sensibility_reset(self):
        self.sensibility = 20000
        self.sensibilitySlider.setValue(self.sensibility)
        self.label_sense.setText(str(self.sensibility))
        aeng.SENSIBILITY = self.sensibility

    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self)
        self.form_initialisation()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())

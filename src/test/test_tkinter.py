### インポート
import tkinter
 
### 入力キー表示関数
def input_key(event):
    key_name = event.keysym
    value.set(key_name)
 
### メイン画面作成
main = tkinter.Tk()
 
### 画面サイズ設定
main.geometry("640x400")
 
### ラベル表示変数
value = tkinter.StringVar()
 
### ラベル作成
label1 = tkinter.Label(master=main, font=(None,24), text="入力キー")
label2 = tkinter.Label(master=main, font=(None,48), fg="red", textvariable=value)
 
### ラベル配置
label1.pack(pady=50)
label2.pack()
 
### キー入力時のイベント取得
label2.bind("<KeyPress>", input_key)
 
### フォーカスセット
label2.focus_set()
 
### イベントループ
main.mainloop()
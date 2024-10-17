import tkinter as tk
from tkinter import messagebox, scrolledtext
import win32com.client

# Função para identificar dispositivos USB conectados
def identificar_dispositivos_usb():
    dispositivos = []
    log_text.delete(1.0, tk.END)  # Limpa o texto anterior no log
    
    try:
        log_text.insert(tk.END, "Tentando acessar o WMI...\n")
        wmi = win32com.client.GetObject('winmgmts:')  # Acessa o WMI para listar dispositivos
        log_text.insert(tk.END, "Acesso ao WMI realizado com sucesso.\n")

        # Verifica se o WMI retornou um objeto válido
        if wmi is not None:
            log_text.insert(tk.END, "Consultando dispositivos conectados...\n")
            # Consulta para listar dispositivos conectados
            for dispositivo in wmi.InstancesOf('Win32_PnPEntity'):
                log_text.insert(tk.END, f"Dispositivo encontrado: {dispositivo.Description}\n")
                if 'USB' in dispositivo.Description:  # Filtra apenas dispositivos USB
                    dispositivos.append(dispositivo.Description)
        else:
            messagebox.showerror("Erro", "Erro ao acessar WMI.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao identificar dispositivos: {type(e).__name__}: {e}")
    
    return dispositivos

# Função para exibir dispositivos na interface
def exibir_dispositivos():
    dispositivos = identificar_dispositivos_usb()
    if dispositivos:
        resultado_texto.set("\n".join(dispositivos))  # Exibe dispositivos na janela
    else:
        resultado_texto.set("Nenhum dispositivo USB conectado.")

# Interface gráfica com Tkinter
janela = tk.Tk()
janela.title("Dispositivos USB Conectados")

resultado_texto = tk.StringVar()

# Título
label_titulo = tk.Label(janela, text="Dispositivos USB Conectados", font=("Helvetica", 16))
label_titulo.pack(pady=10)

# Botão para verificar os dispositivos conectados
botao = tk.Button(janela, text="Verificar Dispositivos", command=exibir_dispositivos)
botao.pack(pady=10)

# Label para exibir o resultado
label_resultado = tk.Label(janela, textvariable=resultado_texto, justify=tk.LEFT, font=("Helvetica", 12))
label_resultado.pack(pady=10)

# Widget de texto para mostrar logs
log_text = scrolledtext.ScrolledText(janela, width=50, height=10, font=("Helvetica", 10))
log_text.pack(pady=10)

# Configuração da janela
janela.geometry("400x400")
janela.mainloop()

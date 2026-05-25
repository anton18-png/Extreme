import tkinter as tk
from tkinter import ttk
import os
import subprocess
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GAME_BAT = os.path.join(BASE_DIR, 'GameMode', 'Игровой режим.bat')
REVERT_BAT = os.path.join(BASE_DIR, 'GameMode', 'Откат игрового режима.bat')

HARDCORE_SERVICES = [
    'AJRouter', 'ALG', 'AarSvc', 'AppIDSvc', 'AppMgmt', 'AppReadiness',
    'AppVClient', 'AppXSvc', 'Appinfo', 'AssignedAccessManagerSvc',
    'AxInstSV', 'BDESVC', 'BFE', 'BITS', 'BTAGService',
    'BcastDVRUserService', 'BluetoothUserService', 'BrokerInfrastructure',
    'BthAvctpSvc', 'CDPSvc', 'CDPUserSvc', 'COMSysApp', 'CaptureService',
    'CertPropSvc', 'ClipSVC', 'ConsentUxUserSvc',
    'CredentialEnrollmentManagerUserSvc', 'CscService', 'DPS',
    'DevQueryBroker', 'DeviceAssociationBrokerSvc', 'DeviceAssociationService',
    'DevicePickerUserSvc', 'DevicesFlowUserSvc', 'DiagTrack',
    'DispBrokerDesktopSvc', 'DisplayEnhancementService', 'DmEnrollmentSvc',
    'Dnscache', 'DoSvc', 'DsSvc', 'DsmSvc', 'DusmSvc', 'EFS', 'Eaphost',
    'EntAppSvc', 'EventLog', 'EventSystem', 'FDResPub', 'FontCache',
    'FontCache3.0.0.0', 'FrameServer', 'GraphicsPerfSvc', 'HvHost',
    'IKEEXT', 'InstallService', 'IpxlatCfgSvc', 'KeyIso', 'KtmRm',
    'LanmanServer', 'LanmanWorkstation', 'LicenseManager', 'LxpSvc',
    'MSDTC', 'MSiSCSI', 'MapsBroker', 'MessagingService',
    'NVDisplay.ContainerLocalSystem', 'NaturalAuthentication', 'NcaSvc',
    'NcbService', 'NcdAutoSetup', 'NetSetupSvc', 'NetTcpPortSharing',
    'Netlogon', 'Netman', 'NgcCtnrSvc', 'NgcSvc', 'NlaSvc',
    'OneSyncSvc', 'PNRPAutoReg', 'PNRPsvc', 'PcaSvc', 'PeerDistSvc',
    'PerfHost', 'PhoneSvc', 'PlugPlay', 'PolicyAgent', 'PrintNotify',
    'PrintWorkflowUserSvc', 'PushToInstall', 'QWAVE', 'RasAuto', 'RasMan',
    'RemoteAccess', 'RemoteRegistry', 'RetailDemo', 'RmSvc', 'RpcLocator',
    'SCPolicySvc', 'SCardSvr', 'SDRSVC', 'SEMgrSvc', 'SENS', 'SNMPTRAP',
    'SSDPSRV', 'SamSs', 'ScDeviceEnum', 'Schedule', 'SecurityHealthService',
    'Sense', 'SensorDataService', 'SensorService', 'SensrSvc', 'SessionEnv',
    'SgrmBroker', 'SharedAccess', 'SharedRealitySvc', 'ShellHWDetection',
    'SmsRouter', 'Spooler', 'SstpSvc', 'StateRepository', 'StorSvc',
    'SysMain', 'TabletInputService', 'TapiSrv', 'TermService', 'Themes',
    'TieringEngineService', 'TimeBrokerSvc', 'TokenBroker', 'TrkWks',
    'TroubleshootingSvc', 'TrustedInstaller', 'UevAgentService',
    'UmRdpService', 'UsoSvc', 'VSS', 'VacSvc', 'VaultSvc', 'W32Time',
    'WEPHOSTSVC', 'WFDSConMgrSvc', 'WManSvc', 'WPDBusEnum', 'WSearch',
    'WaaSMedicSvc', 'WalletService', 'WarpJITSvc', 'WbioSrvc', 'WdNisSvc',
    'WdiServiceHost', 'WdiSystemHost', 'WebClient', 'Wecsvc', 'WerSvc',
    'WiaRpc', 'WinDefend', 'WinHttpAutoProxySvc', 'WinRM', 'WlanSvc',
    'WpcMonSvc', 'WpnService', 'WpnUserService', 'WwanSvc',
    'XblAuthManager', 'XblGameSave', 'XboxGipSvc', 'XboxNetApiSvc',
    'autotimesvc', 'bthserv', 'cbdhsvc', 'defragsvc',
    'diagnosticshub.standardcollector.service', 'dmwappushservice',
    'dot3svc', 'embeddedmode', 'fdPHost', 'fhsvc', 'hidserv', 'icssvc',
    'iphlpsvc', 'lfsvc', 'lltdsvc', 'lmhosts', 'mpssvc', 'msiserver',
    'netprofm', 'p2pimsvc', 'p2psvc', 'perceptionsimulation', 'pla',
    'seclogon', 'shpamsvc', 'smphost', 'spectrum', 'stisvc', 'svsvc',
    'swprv', 'tzautoupdate', 'upnphost', 'vds', 'vmicguestinterface',
    'vmicheartbeat', 'vmickvpexchange', 'vmicrdv', 'vmicshutdown',
    'vmictimesync', 'vmicvmsession', 'vmicvss', 'wbengine', 'wcncsvc',
    'wercplsupport', 'wisvc', 'wlidsvc', 'wlpasvc', 'wmiApSrv', 'wscsvc',
    'wuauserv',
]

RECOMMENDED_SERVICES = [
    ('ALG', 3), ('AppIDSvc', 3), ('Appinfo', 3), ('AppMgmt', 3),
    ('AppReadiness', 3), ('AppXSvc', 3), ('AudioEndpointBuilder', 2),
    ('Audiosrv', 2), ('BFE', 3), ('BITS', 4), ('BrokerInfrastructure', 2),
    ('BTAGService', 4), ('BDESVC', 4), ('camsvc', 3), ('CDPSvc', 4),
    ('ClipSVC', 2), ('COMSysApp', 3), ('CoreMessagingRegistrar', 2),
    ('cphs', 4), ('cplspcon', 4), ('CryptSvc', 2), ('DcomLaunch', 2),
    ('DeviceAssociationService', 3), ('DeviceInstall', 3),
    ('DevQueryBroker', 3), ('Dhcp', 2),
    ('diagnosticshub.standardcollector.service', 4), ('diagsvc', 4),
    ('diagtrack', 4), ('DispBrokerDesktopSvc', 4),
    ('DisplayEnhancementService', 3), ('DmEnrollmentSvc', 3),
    ('Dnscache', 2), ('DoSvc', 4), ('dot3svc', 3), ('DPS', 4),
    ('DsmSvc', 3), ('DsSvc', 3), ('Eaphost', 3), ('EFS', 4),
    ('EventLog', 2), ('EventSystem', 2), ('fdPHost', 3), ('FDResPub', 3),
    ('FontCache', 4), ('FontCache3.0.0.0', 3), ('FrameServer', 3),
    ('gpsvc', 2), ('GraphicsPerfSvc', 3), ('hidserv', 3), ('IKEEXT', 2),
    ('InstallService', 3), ('iphlpsvc', 2), ('IpxlatCfgSvc', 3),
    ('KAPSService', 4), ('KeyIso', 3), ('KNDBWM', 4), ('KtmRm', 3),
    ('LanmanServer', 4), ('LanmanWorkstation', 4), ('LicenseManager', 3),
    ('lmhosts', 4), ('lfsvc', 4), ('LSM', 2), ('LxpSvc', 3),
    ('mpssvc', 2), ('MSDTC', 3), ('NcbService', 3), ('NcdAutoSetup', 3),
    ('Netman', 3), ('netprofm', 3), ('NetSetupSvc', 3),
    ('NetTcpPortSharing', 4), ('NgcCtnrSvc', 3), ('NgcSvc', 3),
    ('NlaSvc', 2), ('nsi', 2), ('p2pimsvc', 3), ('p2psvc', 3),
    ('PcaSvc', 3), ('PerfHost', 3), ('pla', 3), ('PlugPlay', 3),
    ('PNRPAutoReg', 3), ('PNRPsvc', 3), ('PolicyAgent', 3), ('Power', 2),
    ('PrintNotify', 3), ('ProfSvc', 2), ('QWAVE', 4), ('RasMan', 2),
    ('RpcEptMapper', 2), ('RpcSs', 2), ('RmSvc', 3), ('SamSs', 2),
    ('Schedule', 2), ('seclogon', 3), ('SecurityHealthService', 4),
    ('Sendevsvc', 2), ('SENS', 4), ('SensorDataService', 3),
    ('SensorService', 3), ('SensrSvc', 3), ('SharedAccess', 3),
    ('ShellHWDetection', 2), ('SNMPTRAP', 3), ('Spooler', 4),
    ('sppsvc', 2), ('SSDPSRV', 4), ('SstpSvc', 3), ('StateRepository', 3),
    ('Steam Client Service', 3), ('stisvc', 3), ('StorSvc', 2),
    ('svsvc', 3), ('swprv', 3), ('SystemEventsBroker', 2),
    ('SgrmBroker', 4), ('TabletInputService', 3), ('Themes', 4),
    ('TimeBrokerSvc', 3), ('TokenBroker', 3), ('TrustedInstaller', 3),
    ('TrkWks', 4), ('upnphost', 3), ('UserManager', 2), ('UsoSvc', 3),
    ('VaultSvc', 3), ('vds', 3), ('vgc', 2), ('VSS', 3), ('W32Time', 3),
    ('WaaSMedicSvc', 3), ('WarpJITSvc', 3), ('Wcmsvc', 2),
    ('WdiServiceHost', 3), ('WdiSystemHost', 3), ('Wecsvc', 3),
    ('WEPHOSTSVC', 3), ('WFDSConMgrSvc', 3), ('WiaRpc', 3),
    ('WinHttpAutoProxySvc', 3), ('Winmgmt', 2), ('WlanSvc', 2),
    ('wlidsvc', 4), ('WManSvc', 3), ('wmiApSrv', 3), ('WSearch', 4),
    ('wuauserv', 4), ('XblAuthManager', 3), ('XblGameSave', 3),
    ('XboxGipSvc', 3), ('XboxNetApiSvc', 3), ('xTendSoftAPService', 4),
    ('xTendUtilityService', 4), ('BcastDVRUserService', 4),
    ('BluetoothUserService', 4), ('CaptureService', 3), ('cbdhsvc', 4),
    ('CDPUserSvc', 2), ('ConsentUxUserSvc', 3),
    ('CredentialEnrollmentManagerUserSvc', 3),
    ('DeviceAssociationBrokerSvc', 3), ('DevicePickerUserSvc', 3),
    ('DevicesFlowUserSvc', 3), ('OneSyncSvc', 4),
    ('PimIndexMaintenanceSvc', 3), ('PrintWorkflowUserSvc', 3),
    ('UdkUserSvc', 3), ('UnistoreSvc', 3),
]


def run_as_admin_async(bat_path, status_callback, done_callback):
    def task():
        status_callback(f"Запуск: {os.path.basename(bat_path)}...")
        try:
            proc = subprocess.Popen(
                [bat_path],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            stdout, stderr = proc.communicate(timeout=300)
            if proc.returncode == 0:
                status_callback("Выполнено успешно.")
            else:
                err = stderr.decode('cp1251', errors='replace').strip()
                status_callback(f"Завершено (код: {proc.returncode})" + (f": {err}" if err else ""))
        except subprocess.TimeoutExpired:
            status_callback("Ошибка: превышено время ожидания (5 мин).")
        except Exception as e:
            status_callback(f"Ошибка: {e}")
        done_callback()
    threading.Thread(target=task, daemon=True).start()


def create_game_mode_tab(tab_control):
    game_tab = ttk.Frame(tab_control)
    tab_control.add(game_tab, text='Игровой режим')

    main_frame = ttk.Frame(game_tab, padding=20)
    main_frame.pack(fill='both', expand=True)

    title = ttk.Label(
        main_frame,
        text='🎮 Игровой режим (Game Mode)',
        font=('Segoe UI', 18, 'bold'),
    )
    title.pack(anchor='w', pady=(0, 5))

    desc = ttk.Label(
        main_frame,
        text='Комплексная оптимизация Windows для максимальной производительности в играх.\n'
             'Объединяет лучшие твики от xOS и два профиля отключения служб.',
        font=('Segoe UI', 9),
        wraplength=900,
        justify='left',
    )
    desc.pack(anchor='w', pady=(0, 15))

    # ── Main horizontal split ──
    hsplit = ttk.PanedWindow(main_frame, orient='horizontal')
    hsplit.pack(fill='both', expand=True)

    # ═══ LEFT: Actions ═══
    left = ttk.Frame(hsplit, padding=(0, 0, 10, 0))
    hsplit.add(left, weight=1)

    action_frame = ttk.LabelFrame(left, text='Действия', padding=15)
    action_frame.pack(fill='x', pady=(0, 10))

    status_var = tk.StringVar(value='Готов к запуску.')
    status_label = ttk.Label(left, textvariable=status_var, wraplength=400)
    status_label.pack(anchor='w', fill='x')

    progress = ttk.Progressbar(left, mode='indeterminate')
    btn_frame = ttk.Frame(action_frame)
    btn_frame.pack(fill='x')

    def set_busy(busy):
        for b in (apply_btn, revert_btn):
            b.configure(state='disabled' if busy else 'normal')
        if busy:
            progress.pack(fill='x', pady=(10, 0))
            progress.start(15)
        else:
            progress.stop()
            progress.pack_forget()

    def on_done():
        set_busy(False)

    def apply_game():
        if not os.path.exists(GAME_BAT):
            status_var.set(f'Файл не найден: {GAME_BAT}')
            return
        set_busy(True)
        run_as_admin_async(GAME_BAT, lambda s: status_var.set(s), on_done)

    def revert_game():
        if not os.path.exists(REVERT_BAT):
            status_var.set(f'Файл не найден: {REVERT_BAT}')
            return
        set_busy(True)
        run_as_admin_async(REVERT_BAT, lambda s: status_var.set(s), on_done)

    apply_btn = ttk.Button(
        btn_frame, text='Применить игровой режим',
        command=apply_game, width=40,
    )
    apply_btn.pack(side='left', padx=(0, 10))

    revert_btn = ttk.Button(
        btn_frame, text='Откатить игровой режим',
        command=revert_game, width=40,
    )
    revert_btn.pack(side='left')

    # ── Warning below actions ──
    warn_frame = ttk.LabelFrame(left, text='⚠️ Внимание', padding=10)
    warn_frame.pack(fill='x', pady=(10, 0))

    warn_text = (
        '• Запускайте от имени Администратора\n'
        '• Рекомендуется создать точку восстановления перед применением\n'
        '• После применения не рекомендуется перезапускать компьютер\n'
        '• Для возврата используйте кнопку "Откатить игровой режим"'
    )
    ttk.Label(warn_frame, text=warn_text, font=('Segoe UI', 8), justify='left').pack(anchor='w')

    # ═══ RIGHT: Detailed info with sub-tabs ═══
    right = ttk.Frame(hsplit, padding=(10, 0, 0, 0))
    hsplit.add(right, weight=2)

    info_notebook = ttk.Notebook(right)
    info_notebook.pack(fill='both', expand=True)

    # ── Tab 1: Описание твиков ──
    tweaks_frame = ttk.Frame(info_notebook, padding=10)
    info_notebook.add(tweaks_frame, text='Описание твиков')

    tweaks_canvas = tk.Canvas(tweaks_frame, highlightthickness=0)
    tweaks_scrollbar = ttk.Scrollbar(tweaks_frame, orient='vertical', command=tweaks_canvas.yview)
    tweaks_scrollable = ttk.Frame(tweaks_canvas)

    tweaks_scrollable.bind('<Configure>', lambda e: tweaks_canvas.configure(scrollregion=tweaks_canvas.bbox('all')))
    tweaks_canvas.create_window((0, 0), window=tweaks_scrollable, anchor='nw')
    tweaks_canvas.configure(yscrollcommand=tweaks_scrollbar.set)
    tweaks_canvas.pack(side='left', fill='both', expand=True)
    tweaks_scrollbar.pack(side='right', fill='y')

    def _on_mousewheel(event):
        tweaks_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
    tweaks_canvas.bind('<MouseWheel>', _on_mousewheel)

    tc = ttk.Frame(tweaks_scrollable)
    tc.pack(fill='both', expand=True)

    sections = [
        ('⚡ Базовые твики xOS (5 шт.)',
         'Отключают фоновые механизмы энергосбережения процессора:\n'
         '• Dynamic Tick — выключает "тики" простоя ядер CPU\n'
         '• Energy Estimation — убирает расчёт энергопотребления\n'
         '• Power Throttling — отключает троттлинг по питанию\n'
         '• Таймауты электропитания — убирает задержки входа/выхода из сна\n'
         '• Отключение диска — запрещает системе отключать HDD/SSD'),
        ('🔌 USB и PCI Express (6 шт.)',
         '• Максимальная производительность USB — запрещает отключение USB\n'
         '• Максимальная производительность PCI Express — запрещает экономию на PCI-E\n'
         '• Отключение журналов диагностики (3 файла) — прекращает логирование'
         ' энергопотребления, сна, режимов питания\n'
         '• Отключение телеметрии USB и USBHUB3'),
        ('🌙 Энергосберегающие функции (24 шт.)',
         'Для новичков (12 шт.): расширенное управление питанием, D3, USB, '
         'Wake-on-LAN, управляемые переходы и т.д.\n'
         'Для профессионалов (12 шт.): AllowIdleIrpInD3, D3ColdSupported, '
         'DeviceSelectiveSuspended, EnableIdlePowerManagement, '
         'EnableSelectiveSuspend, EnhancedPowerManagementEnabled, '
         'IdleInWorkingState, SelectiveSuspendEnabled/On, '
         'WaitWakeEnabled, WakeEnabled, WdfDirectedPowerTransitionEnable'),
        ('📋 Службы (хардкор) — >200 служб',
         'Первый батник устанавливает Start=4 (отключено) практически всем '
         'некритическим службам Windows. Аудио, сеть и базовые службы '
         'остаются включёнными.\n'
         'Второй батник дополнительно отключает PimIndexMaintenanceSvc, '
         'UnistoreSvc, UserDataSvc, CDPUserSvc и удаляет diagsvc.'),
        ('📋 Службы (рекомендованные) — >150 служб',
         'Более сбалансированный профиль: часть служб выключается (4), '
         'часть переводится в ручной режим (3), критичные остаются '
         'автоматическими (2).\n'
         'Второй батник (аналогичен хардкорному) — те же 4 службы + diagsvc.'),
    ]

    for title, body in sections:
        sec = ttk.LabelFrame(tc, text=title, padding=8)
        sec.pack(fill='x', pady=(0, 10))
        ttk.Label(sec, text=body, wraplength=600, justify='left',
                  font=('Segoe UI', 8)).pack(anchor='w')

    # ── Tab 2: Отключаемые службы ──
    services_frame = ttk.Frame(info_notebook, padding=10)
    info_notebook.add(services_frame, text='Отключаемые службы')

    svc_notebook = ttk.Notebook(services_frame)
    svc_notebook.pack(fill='both', expand=True)

    # Hardcore tab
    hc_frame = ttk.Frame(svc_notebook, padding=8)
    svc_notebook.add(hc_frame, text='Хардкор')

    hc_canvas = tk.Canvas(hc_frame, highlightthickness=0)
    hc_sbar = ttk.Scrollbar(hc_frame, orient='vertical', command=hc_canvas.yview)
    hc_inner = ttk.Frame(hc_canvas)
    hc_inner.bind('<Configure>', lambda e: hc_canvas.configure(scrollregion=hc_canvas.bbox('all')))
    hc_canvas.create_window((0, 0), window=hc_inner, anchor='nw')
    hc_canvas.configure(yscrollcommand=hc_sbar.set)
    hc_canvas.pack(side='left', fill='both', expand=True)
    hc_sbar.pack(side='right', fill='y')
    hc_canvas.bind('<MouseWheel>', lambda e: hc_canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))

    ttk.Label(hc_inner, text='Start=4 (отключены). Audio и критические службы не трогаются.',
              font=('Segoe UI', 8, 'bold'), foreground='orange').pack(anchor='w', pady=(0, 5))

    # Display as columns
    hc_col_frame = ttk.Frame(hc_inner)
    hc_col_frame.pack(fill='both', expand=True)

    col_size = 60
    cols = [HARDCORE_SERVICES[i:i+col_size] for i in range(0, len(HARDCORE_SERVICES), col_size)]
    for col in cols:
        f = ttk.Frame(hc_col_frame)
        f.pack(side='left', fill='y', padx=(0, 15))
        for svc in col:
            ttk.Label(f, text=svc, font=('Consolas', 7)).pack(anchor='w')

    # Recommended tab
    rec_frame = ttk.Frame(svc_notebook, padding=8)
    svc_notebook.add(rec_frame, text='Рекомендованные')

    rec_canvas = tk.Canvas(rec_frame, highlightthickness=0)
    rec_sbar = ttk.Scrollbar(rec_frame, orient='vertical', command=rec_canvas.yview)
    rec_inner = ttk.Frame(rec_canvas)
    rec_inner.bind('<Configure>', lambda e: rec_canvas.configure(scrollregion=rec_canvas.bbox('all')))
    rec_canvas.create_window((0, 0), window=rec_inner, anchor='nw')
    rec_canvas.configure(yscrollcommand=rec_sbar.set)
    rec_canvas.pack(side='left', fill='both', expand=True)
    rec_sbar.pack(side='right', fill='y')
    rec_canvas.bind('<MouseWheel>', lambda e: rec_canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))

    ttk.Label(rec_inner, text='Start=2 (авто) / 3 (вручную) / 4 (отключено)',
              font=('Segoe UI', 8, 'bold'), foreground='cyan').pack(anchor='w', pady=(0, 5))

    legend = ttk.Frame(rec_inner)
    legend.pack(anchor='w', pady=(0, 8))
    for txt, color in [('Start=2 — Авто', '#00ff00'), ('Start=3 — Вручную', 'yellow'), ('Start=4 — Отключено', '#ff6666')]:
        ttk.Label(legend, text=txt, foreground=color, font=('Segoe UI', 7, 'bold')).pack(side='left', padx=(0, 12))

    rec_col_frame = ttk.Frame(rec_inner)
    rec_col_frame.pack(fill='both', expand=True)

    rcol_size = 40
    rcols = [RECOMMENDED_SERVICES[i:i+rcol_size] for i in range(0, len(RECOMMENDED_SERVICES), rcol_size)]
    for col in rcols:
        f = ttk.Frame(rec_col_frame)
        f.pack(side='left', fill='y', padx=(0, 15))
        for svc, val in col:
            color = '#00ff00' if val == 2 else ('yellow' if val == 3 else '#ff6666')
            ttk.Label(f, text=f'{svc}  ({val})', font=('Consolas', 7),
                      foreground=color).pack(anchor='w')

    # ── Tab 3: Плюсы/Минусы ──
    pros_frame = ttk.Frame(info_notebook, padding=10)
    info_notebook.add(pros_frame, text='Плюсы и минусы')

    pros_canvas = tk.Canvas(pros_frame, highlightthickness=0)
    pros_sbar = ttk.Scrollbar(pros_frame, orient='vertical', command=pros_canvas.yview)
    pros_inner = ttk.Frame(pros_canvas)
    pros_inner.bind('<Configure>', lambda e: pros_canvas.configure(scrollregion=pros_canvas.bbox('all')))
    pros_canvas.create_window((0, 0), window=pros_inner, anchor='nw')
    pros_canvas.configure(yscrollcommand=pros_sbar.set)
    pros_canvas.pack(side='left', fill='both', expand=True)
    pros_sbar.pack(side='right', fill='y')
    pros_canvas.bind('<MouseWheel>', lambda e: pros_canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))

    pc = ttk.Frame(pros_inner)
    pc.pack(fill='both', expand=True)

    pros_section = ttk.LabelFrame(pc, text='✅ Плюсы', padding=10)
    pros_section.pack(fill='x', pady=(0, 15))

    pros_text = (
        '1. Максимальная производительность CPU — отключены фоновые замеры '
        'энергопотребления (Energy Estimation, Power Throttling, Dynamic Tick)\n\n'
        '2. Снижение задержек (input lag) — отключены механизмы энергосбережения, '
        'которые вызывают микротормоза\n\n'
        '3. Минимальное фоновое потребление ресурсов — отключено >200 служб, '
        'включая телеметрию, Xbox, Bluetooth, принтеры\n\n'
        '4. Высвобождение ОЗУ — десятки служб больше не висят в памяти\n\n'
        '5. Уменьшение количества потоков и прерываний — CPU меньше переключается '
        'между задачами\n\n'
        '6. Полный контроль — можно откатить одним батником\n\n'
        '7. Подходит для слабых ПК и ноутбуков — снижает нагрузку на железо'
    )
    ttk.Label(pros_section, text=pros_text, wraplength=650, justify='left',
              font=('Segoe UI', 8)).pack(anchor='w')

    cons_section = ttk.LabelFrame(pc, text='❌ Минусы', padding=10)
    cons_section.pack(fill='x', pady=(0, 15))

    cons_text = (
        '1. Не работает Bluetooth — служба BthAvctpSvc, bthserv отключены\n\n'
        '2. Не работают принтеры — Spooler отключён (можно включить вручную)\n\n'
        '3. Не работают Xbox/игровые аксессуары — XboxGipSvc и связанные службы отключены\n\n'
        '4. Не работает автообновление Windows — wuauserv отключена\n\n'
        '5. Может перестать работать VPN — RasMan, IKEEXT отключены\n\n'
        '6. Не работает поиск Windows — WSearch отключена\n\n'
        '7. Отключена телеметрия — некоторые приложения могут "жаловаться"\n\n'
        '8. Удаляется служба diagsvc — диагностическая служба Windows\n\n'
        '9. Возможны проблемы с Wi-Fi на некоторых адаптерах — WlanSvc включена, '
        'но может потребоваться дополнительная настройка\n\n'
        '10. Не рекомендуется для ноутбуков — батарея будет разряжаться быстрее'
    )
    ttk.Label(cons_section, text=cons_text, wraplength=650, justify='left',
              font=('Segoe UI', 8)).pack(anchor='w')

    neutral_section = ttk.LabelFrame(pc, text='⚖️ Нюансы', padding=10)
    neutral_section.pack(fill='x')

    neutral_text = (
        '• Гибернация и план питания xOS не затрагиваются\n'
        '• Контекстное меню не изменяется\n'
        '• Службы аудио (AudioEndpointBuilder, Audiosrv) остаются включёнными\n'
        '• Брандмауэр (mpssvc) включён — безопасность не страдает\n'
        '• Рекомендуется периодически проверять целостность системных файлов\n'
        '• После обновлений Windows некоторые службы могут включиться заново'
    )
    ttk.Label(neutral_section, text=neutral_text, wraplength=650, justify='left',
              font=('Segoe UI', 8)).pack(anchor='w')

    return game_tab

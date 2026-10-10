# ALLOH UCHUN

> Har kuni bir qadam. Sabr, intizom va Alloh roziligi uchun.

Windows 10/11 uchun shaxsiy kunlik intizom kuzatuvchisi (Python 3 + PySide6 + SQLite).
Barcha ma'lumotlar **faqat sizning kompyuteringizda** saqlanadi; ilova internetga hech narsa yubormaydi.

## Imkoniyatlar
- Haqiqiy oylik kalendar (28/29/30/31 kun, kabisa yillari), oylar bo'ylab yurish, har qanday o'tgan kunni tanlash.
- Holatlar: **Muvaffaqiyat**, **Qiyin kun**, **Maqsad buzildi** + ixtiyoriy shaxsiy izoh.
- «Qiyin kun» uchun alohida tasdiq: **Ha / Yo‘q / Hali aniqlashtirmayman** (holatdan alohida saqlanadi).
- Statistika, seriyalar, oylar tarixi.
- Saqlangandan keyin motivatsion xabar va amaliy sinov; **Bugungi sinov** (bajarish / o‘tkazib yuborish / keyinroqqa).
- **HOZIR O‘ZIMNI NAZORAT QILISHIM KERAK** — 10 daqiqalik qo'llab-quvvatlovchi reja.
- Zaxira nusxa, tiklash, barcha yozuvlarni o'chirish (tasdiq dialogi bilan).
- Har bir saqlash darhol SQLite bazasiga yoziladi (avtomatik saqlash). Yozilmagan kunlar yozilmagan holda qoladi.

## Statistika qoidalari (aniq hisoblash)
1. **Tasdiqlangan muvaffaqiyatli kun** — faqat quyidagilar:
   - holati «Muvaffaqiyat» bo'lgan kun, **yoki**
   - holati «Qiyin kun» va tasdig'i aniq **«Ha»** bo'lgan kun.
   «Yo‘q», «Hali aniqlashtirmayman», «Maqsad buzildi» va yozilmagan kunlar **hech qachon** muvaffaqiyat hisoblanmaydi.
2. **Yozilgan kunlar** — tanlangan oyda yozuvi bor kunlar soni.
3. **Qiyin kunlar / Maqsad buzilgan kunlar** — shu oyda tegishli holat bilan yozilgan kunlar (tasdig'idan qat'i nazar).
   Tasdig'i «Ha» bo'lgan qiyin kun ham «Qiyin kunlar»da, ham «tasdiqlangan muvaffaqiyatli kunlar»da sanaladi.
4. **Oylik muvaffaqiyat foizi** = tasdiqlangan muvaffaqiyatli kunlar ÷ shu oydagi **yozilgan** kunlar × 100
   (bir kasrgacha). Yozuv bo'lmasa, «—» ko'rsatiladi (0% emas). Yozilmagan kunlar maxrajga kirmaydi va muvaffaqiyat deb olinmaydi.
5. **Eng uzun seriya** — tasdiqlangan muvaffaqiyatli kunlarning ketma-ket **kalendar sanalari** bo'yicha eng uzun zanjiri
   (oy, yil va 29-fevral chegaralaridan o'tadi). Bitta yozilmagan sana yoki tasdiqlanmagan natija zanjirni uzadi.
6. **Joriy seriya** — bugundan orqaga qarab hisoblanadigan shunday zanjir uzunligi:
   - bugun tasdiqlangan muvaffaqiyat bo'lsa, bugundan boshlanadi;
   - bugun umuman yozilmagan bo'lsa, kechadan boshlanadi (kun hali tugamagan, seriya uzilmaydi, lekin bugun sanalmaydi);
   - bugun yozilgan, ammo muvaffaqiyat emas/tasdiqlanmagan bo'lsa, joriy seriya **0**.

## Ma'lumotlar joyi
`%APPDATA%\ALLOH_UCHUN\alloh_uchun.db` (yozish mumkin bo'lgan papka). Linux/test uchun `ALLOH_UCHUN_DATA_DIR`
muhit o'zgaruvchisi bilan almashtirish mumkin. Tiklash yaroqsiz faylni rad etadi va joriy ma'lumotlarni o'zgartirmaydi.

## Iqtiboslar haqida
Faqat matni va manbasi ishonchli bo'lgan oyat/hadislar «ma’nosi» sifatida berilgan (Inshirah 94:5–6, Baqara 2:153,
Zumar 39:53, Sahih al-Buxoriy 1 / Sahih Muslim 1907). Qo'shishdan oldin manbani albatta tekshiring.
Ilova tibbiy yoki psixologik yordam o'rnini bosmaydi; o'zingizga zarar yetkazish fikrlari bo'lsa, yaqinlaringiz yoki mutaxassisga murojaat qiling.

## Ishga tushirish (dasturchi uchun)
```
pip install -r requirements.txt
python main.py
python -m pytest -q
```

## Windows .exe yig'ish
Windows 10/11 da, loyiha papkasida:
```
build_windows.bat
```
Natija: `dist\ALLOH_UCHUN.exe` (Python o'rnatish shart emas). PyInstaller boshqa OS uchun kross-kompilyatsiya qilmaydi,
shuning uchun `.exe` faqat Windows'da yig'iladi.

## Tuzilma
```
main.py                     kirish nuqtasi
alloh_uchun/models.py       modellar (Status, Confirmation, DayEntry)
alloh_uchun/database.py     SQLite, zaxira/tiklash
alloh_uchun/calendar_logic.py, stats.py
alloh_uchun/motivation.py   xabarlar, sinovlar, 10 daqiqalik reja
alloh_uchun/ui/             interfeys (tema, kalendar, dialoglar, asosiy oyna)
tests/                      testlar
ALLOH_UCHUN.spec, build_windows.bat
```

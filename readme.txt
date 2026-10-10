========================================================================
 HEAD-HUNTER BACKEND - KOD BAHOLASH (TAHLIL)
 Loyiha: Head-Hunter (Django 6.1 + DRF + SimpleJWT)
 Tekshirilgan: 2026-10-10
 Usul: har bir app manba kodi to'liq o'qildi + `manage.py check`,
       `makemigrations --check`, model introspeksiyasi.
========================================================================

UMUMIY BALL: 43 / 100  (KUCHSIZ / KATTA TUZATISHLAR KERAK)

Autentifikatsiya oqimi eng kuchli va asosan ishlaydi. Asosiy biznes
applar (companies, applications) hozir BUZILGAN: ular mavjud
bo'lmagan model maydonlariga murojaat qiladi, shuning uchun har qanday
runtime chaqiruvda AttributeError / FieldError chiqadi. Shuningdek,
bitta xavfli bug (vacancy o'chirish) va settingsda bir nechta
xavfsizlik muammosi bor. Butun loyihada BIRORTA avtomatik test yo'q.

Har bir app uchun bally:
  core (loyiha sozlamalari) ... 55 / 100
  baseapp ..................... 60 / 100
  authentication .............. 70 / 100
  resumes ..................... 55 / 100
  chat ........................ 45 / 100
  vacancies ................... 40 / 100
  applications ................ 30 / 100
  companies ................... 25 / 100

========================================================================
 1. core (settings.py, urls.py) ....................... 55 / 100
========================================================================
YAXSHI
  - INSTALLED_APPS toza, SimpleJWT rotation + blacklist bilan
    sozlangan.
  - dotenv ishlatilgan; AUTH_USER_MODEL to'g'ri o'rnatilgan.

XATOLAR
  - settings.py:26 SECRET_KEY sukut bo'yicha '' -> .env bo'lmasa ilova
    bo'sh kalit bilan ishga tushadi.
  - settings.py:29 DEBUG = True qattiq yozilgan (env'dan olinishi kerak).
  - settings.py:31 ALLOWED_HOSTS = [] (har qanday haqiqiy deployni
    buzadi).
  - settings.py:158 "MAILERS" - bu Django setting emas; u
    EMAIL_BACKEND bo'lishi kerak. Shu sababli console email backend
    hech qachon ishlamaydi.
  - settings.py:148,150 STATIC_URL / MEDIA_URL oldida slash yo'q
    ('static/', 'media/'). '/static/', '/media/' bo'lishi kerak.
  - django-cors-headers o'rnatilgan, lekin "corsheaders"
    INSTALLED_APPSda yo'q va CorsMiddleware MIDDLEWAREdan yo'q.
  - REST_FRAMEWORKda DEFAULT_PERMISSION_CLASSES yo'q (sukut AllowAny)
    va DEFAULT_PAGINATION_CLASS ham yo'q.
  - urls.py:25,27 companies va applications marshrutlari izohlangan
    (comment), shuning uchun bu applar HTTP orqali ochilmaydi.
  - requirements.txt UTF-16 formatida saqlangan (read tool uni binary
    deb ko'radi); oddiy UTF-8 bo'lishi kerak.
  - Logging yo'q, dev/prod bo'linishi yo'q, throttling yo'q.

========================================================================
 2. baseapp (umumiy modellar/utils/permissions) ....... 60 / 100
========================================================================
YAXSHI
  - BaseModel (UUID pk + created_at) yaxshi qayta ishlatiladigan
    pattern.
  - Umumiy javob yordamchilari (success_response / error_response) va
    validatorlar kodni DRY qiladi.

XATOLAR
  - utils.py:7 va utils.py:72 -> code_generate() IKKI marta
    aniqlangan (keraksiz nusxa).
  - utils.py:15 name_validator(name, type): `type` parametri o'rnatilgan
    type() funksiyasini bosib ketadi (shadowing).
  - models.py: Lang va Category BaseModeldan meros OLMAYDI, Region/
    District/Skill esa oladi. id turlari mos emas (BigAuto va UUID) va
    Lang/Categoryda created_at yo'q.
  - models.py:12 Regionda `parent` yo'q, garchi eski spec (readme)
    region -> district ni parent orqali tasvirlagan bo'lsa ham. Aslida
    bog'lanish District.region da; spec eskirgan.
  - permissions.py:6,11 IsOwnerOrReadOnly / IsOwnerStrict `obj.user`ni
    nazarda tutadi. Company/Chat uchun to'g'ri, lekin boshqa modellar
    owner/employee nomlarini ishlatgani uchun chalkash (companies/
    applications buglariga qarang).
  - Test yo'q.

========================================================================
 3. authentication .................................... 70 / 100
========================================================================
YAXSHI
  - Toza 3 bosqichli ro'yxatdan o'tish (signup -> verify-code ->
    create-account) TempUser + MyToken bilan. secrets yaxshi
    ishlatilgan.
  - JWT login/logout token blacklisting bilan; profile GET/PATCH.

XATOLAR
  - utils.py:46 password_validator belgilar sinflarini tekshiradi, lekin
    UZUNLIKNI emas; Django'ning AUTH_PASSWORD_VALIDATORS lari
    create_user() da ishlamaydi, shuning uchun qisqa parollar qabul
    qilinadi.
  - serializers.py:153 ProfileSerializerda validate_username() bor,
    lekin `username` Meta.fieldsda yo'q, shuning uchun u hech qachon
    chaqirilmaydi (o'lik kod) va foydalanuvchi username'ni
    o'zgartira olmaydi.
  - models.py:26 TempUser.email unique emas va CustomUser.email ham
    unique emas (AbstractUser sukuti). Ro'yxatdan o'tishda ikki akkaunt
    bir xil emailga ega bo'lishi mumkin -> ma'lumot yaxlitligi xavfi.
  - serializers.py:56 `if temp_user.code != code:` temp_user None
    bo'lsa AttributeError beradi; faqat validate_emailda himoyalangan,
    lekin validate() qayta so'rov qiladi va qayta tekshirmaydi.
  - serializers.py:33 VerifyCodeSerializer token max_length=32, holbuki
    generate_token() ~43 belgi ishlab chiqaradi (token_urlsafe(32)).
    Bugun zararsiz, chunki `token` read-only.
  - views.py:88 GetUser'da permission klassi yo'q (DRF sukuti AllowAny)
    - ataylab, lekin aniq AllowAny yozish arziydi.
  - Test yo'q.

========================================================================
 4. resumes ........................................... 55 / 100
========================================================================
YAXSHI
  - Har bir foydalanuvchiga bitta resume (OneToOne), related_name va
    Language'dagi unique_together yaxshi.
  - Skill qo'shish/o'chirish oqimi yaxshi.

XATOLAR
  - views.py:41 `if not resume.is_public and ...` None tekshiruvidan
    OLDIN ishlaydi; agar resume mavjud bo'lmasa, `resume` None bo'ladi
    va bu 404 o'rniga AttributeError (500) beradi.
  - views.py:30,80,90,109,129,140 -> `request.user.resume` foydalanuvchida
    hali resume bo'lmasa RelatedObjectDoesNotExist ko'taradi.
    ResumeCreateAPIView.patch, EducationEdit, ExperienceEdit,
    LanguageAdd ("if not request.user.resume") va LanguageEdit'da
    uchraydi. Do'stona 404/400 bilan ishlanishi kerak.
  - models.py:21 `institution = models.CharField()` va
    models.py:23 `degree = models.CharField(...)` da max_length YO'Q.
    Django 6.1 `check`ni o'tkazadi, lekin bu nozik/portativ emas va
    boshqa DB backendlarda buziladi; har doim max_length yozing.
  - Spec farqi: eski readme Education.start_year/end_year va
    WorkExperience ni tasvirlagan, kod esa start_date/end_date va
    Experience ni amalga oshirgan. Doc va kodni moslashtiring.
  - ResumeSerializerda M2M `skills` read-only (/skills orqali
    boshqariladi), lekin `category` serializerda umuman yo'q, shuning
    uchun category API orqali hech qachon o'rnatilmaydi.
  - Pagination yo'q; test yo'q.

========================================================================
 5. vacancies ......................................... 40 / 100
========================================================================
YAXSHI
  - Ommaviy ro'yxat ACTIVE bo'yicha filtrlaydi va "my vacancies"
    (shaxsiy) endpointlar bor; detail/update'da owner tekshiruvi bor.

XATOLAR
  - views.py:34 XAVFLI BUG: delete() `Vacancy.objects.filter().first()`
    ishlatadi va pk URL argumentini e'tiborsiz qoldiradi.
    DELETE /vacancy/<pk> bazadagi BIRINCHI vacancyni o'chiradi,
    so'ralganini emas.
  - models.py:28 `expires_at = models.DateTimeField(auto_now=True)`
    noto'g'ri: auto_now HAR saqlashda qiymatni qayta yozadi. Tugash
    sanasi bir marta o'rnatilishi kerak (masalan published_at + muddat).
    Shu sababli companies/applicationsdagi expiry tekshiruvi ma'nosiz.
  - models.py:27 published_at yaratishda hech qachon o'rnatilmaydi
    (serializer uni read-only qilgan), ammo ommaviy ro'yxat
    '-published_at' bo'yicha tartiblaydi, ya'ni tartib aslida
    tasodifiy/null.
  - views.py:20 ommaviy ro'yxat muddati o'tgan vacancylarni ajratmaydi
    (expires_at filtri yo'q), CompanyVacanciesViewdan farqli.
  - serializers.py:10 `company` yoziladigan (writable) va create view
    company so'rov yuboruvchi foydalanuvchiga tegishli ekanini
    TEKSHIRMAYDI. Har qanday ish beruvchi boshqa kompaniya nomidan
    vakansiya joylashi mumkin.
  - views.py:46 noto'g'ri xabar: Vacancy PATCHda "Resume not found".
  - Maosh validatsiyasi yo'q (salary_from > salary_to), pagination
    yo'q, admin.py Vacancyni ro'yxatga olmagan. Test yo'q.

========================================================================
 6. chat .............................................. 45 / 100
========================================================================
YAXSHI
  - Chat/Message modeli sender + message_type bilan oqilona dizayn;
    ro'yxat uchun Mini serializerlar yaxshi yechim.

XATOLAR
  - views.py:7 `MessageCreateAPIView.post(self, request, pk)` `pk`ni
    talab qiladi, lekin urls.py:7 `path('message', ...)` da pk YO'Q.
    Xabar yuborish har safar TypeError (500) beradi.
  - serializers.py:48 ChatSerializer.validate() da return yo'q ->
    None qaytaradi. DRF attrs kutadi, shuning uchun Chat yaratish
    buziladi. Bundan tashqari Chat yaratadigan endpoint umuman yo'q
    (ChatSerializer amalda ishlatilmaydi); chat yaratish yo'q.
  - serializers.py:36 `validate_employee` - maydon nomi noto'g'ri
    (maydon `user`), shuning uchun bu validatsiya HECH QACHON
    ishlamaydi.
  - views.py:22 Agar chat mavjud bo'lmasa, `chat` None bo'ladi va u
    baribir serializer contextiga uzatiladi (404 yo'q) -> "Chat not
    found" o'rniga chalkash xatolar.
  - serializers.py:45,78 `sender.user_role not in
    CustomUser.UserRole.choices` - satrni tuplelar ro'yxati bilan
    solishtiradi -> har doim True. Mantiq amalda o'lik.
  - models.py:3 va models.py:6 Application ikki marta import qilingan
    (takror).
  - ChatMiniEmployeeSerializer.get_last_message chatda xabar bo'lmasa
    MessageMiniSerializer(None) quradi; get_context esa qisqa matnga
    ham har doim "..." qo'shadi.
  - Xabarlarda pagination yo'q; test yo'q.

========================================================================
 7. applications ...................................... 30 / 100
========================================================================
YAXSHI
  - O'ylangan model: unique (vacancy, resume), status o'tishlari
    niyati, indekslar, employer/employee filtrlash.

XATOLAR (asosan "maydon mavjud emas")
  - Resume'da `user` maydoni bor, `employee` EMAS. Runtimeda
    tasdiqlandi: Resume.employee mavjud emas. Lekin:
      models.py:30  __str__ self.resume.employee ishlatadi -> AttributeError
      serializers.py:18,74,134,145,153,159 resume.employee ishlatadi
      views.py:36,73 filter(resume__employee=user)
    Bulardan har biri FieldError/AttributeError ko'taradi.
  - Company'da `user` maydoni bor, `owner` EMAS. Lekin:
      views.py:38,76 filter(vacancy__company__owner=user)
      permissions.py:17 vacancy.company.owner
    Bular ham buziladi.
  - models.py:33 can_change_to() self.TRANSITIONS ni o'qiydi, lekin
    TRANSITIONS hech qachon aniqlanmagan -> har status o'zgarishida
    AttributeError. Tasdiqlandi: Application'da TRANSITIONS atributi
    yo'q.
  - urls.py:8-12 <int:id>/<int:pk> ishlatadi, lekin Application/Vacancy
    pk lari UUID. Marshrutlar hech qachon mos kelmaydi (404).
  - App marshrutlanmagan (core/urls.py:27 izohlangan), shuning uchun
    bularning hech biri runtime'da sinalmagan.
  - models.py clean() turkcha satr ishlatadi va DRF create'da
    chaqirilmaydi; serializer tekshiruvi bilan takrorlanadi.
  - Test yo'q.

TUZATISH TARTIBI: Resume.employee -> Resume.user (yoki property
qo'shish), Company.owner -> Company.user (yoki property), TRANSITIONS
ni aniqlash, URL konverterlarini <uuid:...> ga o'zgartirish.

========================================================================
 8. companies ......................................... 25 / 100
========================================================================
YAXSHI
  - View qatlami aslida yaxshi tuzilgan (pagination, filter, search,
    multipart parsing, verify endpoint, vacancies sub-list).

XATOLAR
  - Model maydoni `user` (models.py:8), lekin serializerlar `owner`ga
    murojaat qiladi (serializers.py:33,43) -> FieldError / maydon emas.
  - Serializerlar `website`ga murojaat qiladi (serializers.py:32,42),
    u Company modelida MAVJUD EMAS.
  - Serializerlar `updated_at`ga murojaat qiladi (serializers.py:34,44),
    u BaseModelda YO'Q (faqat created_at).
  - RegionRelation: serializerlar RegionShortSerializer'ni `Region`ga
    bog'laydi, lekin Company.region `District`ga ishora qiladi.
    District'ni Region serializeri bilan serializatsiya qilish
    buziladi/noto'g'ri ma'lumot qaytaradi.
  - Shu sababli CompanyDetailSerializer / CompanyCreateUpdateSerializer
    yozilganidek ishlatib bo'lmaydi.
  - views.py:64 `serializer.save(owner=...)` -> TypeError, noma'lum
    maydon.
  - urls.py BO'SH va app core/urls.pyga qo'shilmagan, shuning uchun
    companies butunlay ochilmaydi. Bu yaxshi view kodi hech qachon
    ishlamagan.
  - models.py:16 __str__ nom o'rniga str(self.id) qaytaradi.
  - Test yo'q.

========================================================================
 UMUMIY (CROSS-CUTTING) MUAMMOLAR
========================================================================
  - TEST YO'Q: har bir tests.py 63 baytli sukut fayl. `manage.py test`
    hech narsani isbotlamaydi. Buzilgan applar shuning uchun
    aniqlanmagan.
  - Applar orasidagi nom mos kelmasligi (user/owner/employee) runtime
    crashlarining asosiy sababi. Bitta konvensiyaga keling.
  - Versiyalangan API (masalan /api/v1/), sxema/docs, throttling yo'q.
  - Xavfsizlik: DEBUG=True, bo'sh SECRET_KEY sukuti, bo'sh
    ALLOWED_HOSTS, CORS yo'q, vacancy create'da kompaniya egaligi
    tekshirilmaydi.
  - `.env` to'g'ri tarzda git-ignore qilingan (git ls-files bilan
    tasdiqlandi); shunday qolsin. Haqiqiy sirlarni commit qilmang.

========================================================================
 TAVSIYA ETILGAN HARAKATLAR REJASI (muhimlik tartibida)
========================================================================
  1. Ma'lumotni yo'q qiluvchi bugni tuzating: vacancies/views.py:34
     delete().
  2. Maydon nomlarini birlashtiring: barcha applar bo'ylab
     user vs owner vs employee.
  3. applications ni tuzating (employee->user, owner->user,
     TRANSITIONS, UUID URL konverterlari) yoki tugallanmagan deb
     tan oling.
  4. companies serializerlarini tuzating (owner/website/updated_at/
     region turi) va urls qo'shib core/urls.pyga ulang.
  5. chat message URLini tuzating (pk qo'shing) va
     ChatSerializer.validate return.
  6. Settingsni to'g'rilang (SECRET_KEY, DEBUG, ALLOWED_HOSTS,
     EMAIL_BACKEND, CORS, URL oldidagi slashlar,
     DEFAULT_PERMISSION_CLASSES).
  7. vacancies expires_at ni tuzating (auto_now olib tashlang) va
     published_at ni o'rnating.
  8. auth, resumes, vacancies, applications uchun testlar qo'shing.
  9. Pagination sukutlarini va API versiyalashni qo'shing.

Yakuniy: 43/100. Arxitektura va papka bo'linishi yaxshi, auth app
deyarli production sifatida, lekin biznes applar crashlar va bitta
buzg'unchi bugga ega, hamda test himoya tarmog'i yo'q. Yuqoridagi
tuzatishlar bilan real ravishda 80+ ga chiqish mumkin.
========================================================================

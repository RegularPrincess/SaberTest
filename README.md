# SaberTest

Задача “Log Streamer”
Имеется log-файл в кодировке UTF-8 и формате JSONL:
{&quot;level&quot;: &quot;DEBUG&quot;, &quot;message&quot;: &quot;Blah blah blah&quot;}
{&quot;level&quot;: &quot;INFO&quot;, &quot;message&quot;: &quot;Everything is fine!&quot;}
{&quot;level&quot;: &quot;WARN&quot;, &quot;message&quot;: &quot;Hmmm, wait...&quot;}
{&quot;level&quot;: &quot;ERROR&quot;, &quot;message&quot;: &quot;Holly $@#t!&quot;}
…
Каждая строка лога — это JSON-объектам с двумя полями:
 level — уровень логирования (может принимать следующие значения: &quot;DEBUG&quot;,
&quot;INFO&quot;, &quot;WARN&quot; и &quot;ERROR&quot;);
 message – произвольный текст с сообщением.
Нужно написать web-сервис, который позволяет последовательно по частям вычитать
данный лог.
Сервис должен корректно работать с приемлемым откликом для любого размера файла
логов (от гигабайта и выше).

На все запросы сервер должен возвращать ответ с кодом 200 и телом в виде JSON-
объекта.

Тело ответа всегда должно содержать булево поле ok, сигнализирующее об успешном
завершении операции, и поле reason с сообщением о причине ошибки – в случае
неудачного выполнения операции, например:
200 {&quot;ok&quot;: true}
200 {&quot;ok&quot;: false, &quot;reason&quot;: &quot;file was not found&quot;}

Запросы в backend
POST /read_log
Чтение лога.
Формат запроса:
{&quot;offset&quot;: &lt;number&gt;}
 offset – позиция, с которой должно быть начато чтение очередной порции лога.
Пример ответа:
{
&quot;ok&quot;: true,
&quot;next_offset&quot;: &lt;number&gt;,
&quot;total_size&quot;: &lt;number&gt;,
&quot;messages&quot;: [
{&quot;level&quot;: &quot;INFO&quot;, &quot;message&quot;: &quot;Everything is fine!&quot;}
{&quot;level&quot;: &quot;WARN&quot;, &quot;message&quot;: &quot;Hmmm, wait... It looks like...&quot;}
{&quot;level&quot;: &quot;ERROR&quot;, &quot;message&quot;: &quot;Holly $@#t!&quot;}
]
}
 next_offset – позиция, с которой должно продолжиться чтение лога.
 total_size – размер всего лога.
 messages – список очередной порции сообщений из лога. В свою очередь,
сообщения являются JSON-объектами, имеющие ту же структуру, что и строки
лога.
В чём измеряются поля offset, next_offset и total_size предлагается решить
самостоятельно.

Взаимодействия с клиентом
При первом обращении к backend&#39;y клиент задаёт значение поля offset равным 0. При
последующих обращениях клиент устанавливает значение offset равным значению
next_offset, которое берётся из тела последнего успешного ответа.
Как только значение поля next_offset становится равным значению поля total_size,
клиент перестаёт посылать запросы к backend&#39;у, и считается, что все сообщения из лога
получены.

Реализация
Следует реализовать сервер для вышеописанного интерфейса.
Для решения следует использовать Python версии 2.7. В качестве фреймворка можно
использовать любой из нижеперечисленного:
 Twisted/Cyclone;
 Tornado;
 Django framework.

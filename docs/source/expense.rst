Expense page handling
=====================

Page is initialized passing the current expense object and the app options that
allows to setup the application.
Then the UI stuff is handled by backbone marionette that synchronises datas to
the server's rest api each time a modification is made on expense lines.

When the user want to re-initialize its expense sheet, or ask for validation, it
passes through the form at the bottom of the screen that is handled by the main
ExpensePage view.

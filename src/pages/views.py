from django.shortcuts import render, redirect
import sqlite3


def login(request, username, password):
    conn = sqlite3.connect('notes.sqlite')
    cursor = conn.cursor()
    response = cursor.execute("SELECT username, password FROM Users WHERE username = :username AND password = :password", {"username": username, "password": password})
    user = response.fetchone()
    if user == None:
        print("incorrect password")
        return False
    else:
        request.session['username'] = username
        return user[0]

def logoutView(request):
    del request.session['username']
    return redirect('/')

def homeView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if login(request, username, password) == username:
            return notesView(request)
    return render(request, 'pages/index.html')

def registerView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #Validating the registered password is not weak
        
        #overused_passwords = [password1, admin/admin...]
        
        #if len(password) < 9 or password.isalpha() == True or password in overused_passwords:
            #return render(request, '/pages/errormessage.html)
        
        conn = sqlite3.connect('notes.sqlite')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (username, password, admin) VALUES (:username, :password, FALSE)", {'username': username, 'password': password})
        conn.commit()
        login(request, username, password)
        return notesView(request)
    if request.method == 'GET':
        return render(request, 'pages/register.html')

def notesView(request):
    username = request.session['username']
    conn = sqlite3.connect('notes.sqlite')
    cursor = conn.cursor()
    response = cursor.execute("SELECT body FROM Notes WHERE owner = :owner AND visible = TRUE", {"owner": username})
    user_notes = response.fetchall()
    correct_notes = []
    for note in user_notes:
        correct_notes.append(note[0])
    response = cursor.execute("SELECT body FROM PublicNotes")
    public_notes = response.fetchall()
    public_notes = list(map(lambda note: note[0], public_notes))
    context = {'notes': correct_notes, 'user': username, 'publicnotes': public_notes}
    return render(request, 'pages/notes.html', context)

def newNoteView(request):
    if request.method == 'POST':
        user = request.session['username']
        note = request.POST.get('note')
        conn = sqlite3.connect('notes.sqlite')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Notes (owner, body, visible) VALUES (:owner, :body, TRUE)", {'owner': user, 'body': note})
        conn.commit()    
        return notesView(request)
    if request.method == 'GET':
        user = request.session['username']
        return render(request, 'pages/newnote.html', context={'user': user})

def publicNoteView(request):
    if request.method == 'POST':
        user = request.session['username']
        note = request.POST.get('publicnote')
        conn = sqlite3.connect('notes.sqlite')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PublicNotes (owner, body) VALUES (:owner, :body)", {'owner': user, 'body': note})
        conn.commit()
        return redirect('/notes')

def noteSearchView(request):
    if request.method == 'POST':
        username = request.session['username']
        note = request.POST.get('note')
        conn = sqlite3.connect('notes.sqlite')
        cursor = conn.cursor()
        
        # This can be used to get bob's password:
        # a"%' UNION SELECT password FROM Users WHERE username = 'bob' OR username LIKE '%"

        response = cursor.execute("SELECT body FROM Notes WHERE owner='" + username + "' AND body like '%" + note + "%'")
        
        # This can be used to fix the vulnerability:
        # response = cursor.execute("SELECT body FROM Notes WHERE owner = :owner AND body LIKE '%' || :body || '%'", {'owner': username, 'body': note})

        search_results = response.fetchall()
        found_notes = list(map(lambda res: res[0], search_results))
        return render(request, 'pages/searchresults.html', context={'notes': found_notes})
    if request.method == 'GET':
        return render(request, 'pages/notesearch.html')

#def is_admin(user):
    #conn = sqlite3.connect('notes.sqlite')
    #cursor = conn.cursor()
    #response = cursor.execute("SELECT admin FROM Users WHERE username = :username", {'username': user})
    #if response.fetchone()[0] == 1:
        #return True
    #else:
        #return False

# Anyone can access admin page to view and delete everyones notes
def adminView(request):
    #if is_admin(request.session.get('username')):
    if request.method == 'GET':
        conn = sqlite3.connect('notes.sqlite')
        cursor = conn.cursor()
        response = cursor.execute("SELECT body, id FROM Notes WHERE visible = TRUE")
        notes = response.fetchall()
        return render(request, 'pages/adminpage.html', context={'notes': notes})
    #else:
        #return render(request, '/pages/error.html', context={'errormessage': 'access denied'})

def deleteView(request, id):
    #if is_admin(request.session.get('username')):
    conn = sqlite3.connect('notes.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE Notes SET visible = FALSE WHERE id = :id", {'id': id})
    conn.commit()
    return redirect('/adminpage')
    #else:
        #return render(request, '/pages/error.html', context={'errormessage': 'access denied'})
import time

call_stack = []
journal = []
journal_level = 0

def OpenJournal(name):
    global call_stack, journal, journal_level
    start_time = time.time()
    call_stack.append(len(journal))
    journal.append((name, journal_level, start_time))
    journal_level = journal_level + 1

def CloseJournal():
    global call_stack, journal, journal_level    
    end_time = time.time()
    index = call_stack[-1]
    del call_stack[-1]
    name, level, start_time = journal[index]
    journal[index] = (name, level, end_time - start_time)
    journal_level = journal_level - 1
    if journal_level == 0: DumpJournal()

def DumpJournal():
    global call_stack, journal, journal_level    
    assert(len(call_stack) == 0)
    for entry in range(0, len(journal)):
        name, level, time = journal[entry]
        print "  " * level, name, round(time, 2)
    journal = []
    
    

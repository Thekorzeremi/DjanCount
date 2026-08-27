from django.shortcuts import render

def event_detail_view(request):
    #MOCK a remplacer avec logique model
    participants = ["Julie", "Seer", "Conambot", "Rémi"]
    
    expenses = [
        {"title": "Pizzas", "amount": 60.0, "payer": "Julie"},
        {"title": "Boissons", "amount": 20.0, "payer": "Rémi"},
        {"title": "Essence", "amount": 40.0, "payer": "Seer"},
    ]

    total_expenses = 0
    balances = {} 

    for expense in expenses:
        total_expenses += expense["amount"]
    
    part_per_pe = 0
    if len(participants) > 0:
        part_per_pe = total_expenses / len(participants)
    
    for participant in participants:
        balances[participant] = -part_per_pe
    
    for expense in expenses:
        payer = expense["payer"]
        if payer in balances: 
            balances[payer] += expense["amount"]

    transactions = []
    debt = []
    initier = []

    for name, sold in balances.items():
        if sold < -0.01:
            debt.append([name, -sold])
        elif sold > 0.01:
            initier.append([name, sold])

    i = 0
    j = 0

    while i < len(debt) and j < len(initier):
        amount_paid = min(debt[i][1], initier[j][1])
        
        transactions.append({
            'from': debt[i][0],
            'to': initier[j][0],
            'amount': round(amount_paid, 2)
        })
        
        debt[i][1] -= amount_paid
        initier[j][1] -= amount_paid
        
        if debt[i][1] <= 0.01:
            i += 1
        if initier[j][1] <= 0.01:
            j += 1

    context = {
        'participants': participants,
        'expenses': expenses,
        'total': total_expenses,
        'part': part_per_pe,
        'balances': balances,
        'transactions': transactions
    }

    return render(request, 'expenses/event_detail.html', context)
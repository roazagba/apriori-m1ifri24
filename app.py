import time
import streamlit as st
import pandas as pd
import itertools
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Apriori - Frequent Itemset Mining",
    page_icon=":house:",
)

def generate_candidate_1(dataset):
    product_dict = {}
    set = []
    for data in dataset:
        for product in data:
            if product not in product_dict:
                product_dict[product] = 1
            else:
                product_dict[product] = product_dict[product] + 1
                
    for key in product_dict:
        array = []
        array.append(key)
        set.append(array)
        set.append(product_dict[key])
        array = []
    return set

def generate_frequent_item_set(list_c, nbr_trans, min_support, dataset, father_frequent_array):
    frequent_items_array, eleminated_items_array = [], []
    for i in range(len(list_c)):
        if i % 2 != 0:
            support = (list_c[i] / nbr_trans) * 100
            if support >= min_support:
                frequent_items_array.append(list_c[i-1])
                frequent_items_array.append(list_c[i])
            else:
                eleminated_items_array.append(list_c[i-1])

    for k in frequent_items_array:
        father_frequent_array.append(k)

    if len(frequent_items_array) in [0, 2]:
        return father_frequent_array
    else:
        display_frequent_item_sets(frequent_items_array)
        generate_candidate_sets(dataset, eleminated_items_array, frequent_items_array, nbr_trans, min_support)
        

def generate_candidate_sets(dataset, eleminated_items_array, frequent_items_array, nbr_trans, min_support):
    only_elements = []
    after_combinaisons = []
    candidate_set_array = []
    for i in range(len(frequent_items_array)):
        if i % 2 == 0:
            only_elements.append(frequent_items_array[i])
            
    for item in only_elements:
        combinaison = []
        k = only_elements.index(item)
        for i in range(k + 1, len(only_elements)):
            for j in item:
                if j not in combinaison:
                    combinaison.append(j)
            for m in only_elements[i]:
                if m not in combinaison:
                    combinaison.append(m)
            after_combinaisons.append(combinaison)
            combinaison = []
            
    sorted_combinaison_array = []
    unique_combinaison_array = []
    for i in after_combinaisons:
        sorted_combinaison_array.append(sorted(i))
        
    for i in sorted_combinaison_array:
        if i not in unique_combinaison_array:
            unique_combinaison_array.append(i)
            
    after_combinaisons = unique_combinaison_array
    for item in after_combinaisons:
        count = 0
        for transaction in dataset:
            if set(item).issubset(set(transaction)):
                count = count + 1
        if count != 0:
            candidate_set_array.append(item)
            candidate_set_array.append(count)
    generate_frequent_item_set(candidate_set_array, nbr_trans, min_support, dataset, father_frequent_array)

def display_frequent_item_sets(frequent_item_sets):
    items_set = []
    for item_set in range(len(frequent_item_sets)):
        if item_set % 2 == 0:
            l = []
            items = ', '.join(frequent_item_sets[item_set])
            support = str(frequent_item_sets[item_set + 1])
            l.append(items)
            l.append(support)
            items_set.append(l)
    dt2 = pd.DataFrame(items_set, columns=["Elements Fréquent", "Support"])
    st.dataframe(dt2, width=1000)
            

def generate_association_rule(frequent_set):
    association_rule = []
    for item in frequent_set:
        if isinstance(item, list):
            if len(item) != 0:
                length = len(item) - 1
                while length > 0:
                    combinations = list(itertools.combinations(item, length))
                    temp = []
                    LHS = []
                    for RHS in combinations:
                        LHS = set(item) - set(RHS)
                        temp.append(list(LHS))
                        temp.append(list(RHS))
                        association_rule.append(temp)
                        temp = []
                    length = length - 1
    return association_rule

def apriori(rules, dataset, min_support, min_confidence):
    output = []
    for rule in rules:
        support_x = 0
        support_y = 0
        support_x_percentage = 0
        support_x_y = 0
        support_x_y_percentage = 0
        for transaction in dataset:
            if set(rule[0]).issubset(set(transaction)):
                support_x = support_x + 1
            if set(rule[1]).issubset(set(transaction)):
                support_y = support_y + 1
            if set(rule[0] + rule[1]).issubset(set(transaction)):
                support_x_y = support_x_y + 1
        support_x_percentage = (support_x / nbr_trans) * 100
        support_x_y_percentage = (support_x_y / nbr_trans) * 100
        confidence = (support_x_y_percentage / support_x_percentage) * 100
        lift = (support_x_y / nbr_trans) / ((support_x / nbr_trans) * (support_y / nbr_trans))
        if confidence >= min_confidence:
            support_x_append_string = str(round(support_x_percentage)) + "%"
            lift_append_string = str(round(lift, 3))
            support_x_y_append_string = str(round(support_x_y_percentage)) + "%"
            confidence_append_string = str(round(confidence)) + "%"

            output.append(support_x_append_string)
            output.append(support_x_y_append_string)
            output.append(confidence_append_string)
            output.append(rule)
            output.append(lift_append_string)

    return output

st.title('Algorithme de Apriori')

file = st.file_uploader('Télécharger le fichier CSV comportant vos données', type='csv')

if file is not None:
    filename = "data/"+str(round(time.time()))+"_file.csv"
    with open(filename, "wb") as f:
        f.write(file.getbuffer())
        
    sep = st.selectbox('Choisir le séparateur des données CSV', ['Cliquer', 'Virgule', 'Point-Virgule'])
    if sep != "Cliquer":
        if sep == "Virgule":
            separator = ","
        elif sep == "Point-Virgule":
            separator = ";"
            
        dataset = []
        
        with open(filename,'r') as fp:
            lines = fp.readlines()

        for line in lines:
            line = line.rstrip()
            dataset.append(line.split(separator))
        
        st.markdown("<hr><h4 style='font-weight:bold;'>Affichage des 10 premières lignes </h4>", unsafe_allow_html=True)
        st.dataframe(dataset[:10])
        
        st.markdown("<hr><h4 style='font-weight:bold;'>Définir le support et le niveau de confiance en %</h4>", unsafe_allow_html=True)
        
        min_support = st.slider("Sélectionnez le support minumum", min_value=5, max_value=100, value=20, step=1)
        min_confidence = st.slider("Sélectionnez le niveau de confiance minimum", min_value=5, max_value=100, value=60, step=1)
        
        min_support = float(min_support)
        min_confidence = float(min_confidence)

        eleminated_items_array = []
        nbr_trans = 0
        father_frequent_array = []

       
        
        dataset_final = [[item for item in sub_list if item != ""] for sub_list in dataset]
        
        nbr_trans = len(dataset_final)

        st.markdown("<hr><h4 style='font-weight:bold;'>Ensemble d'éléments fréquents</h4>", unsafe_allow_html=True)
        first_candidate_set = generate_candidate_1(dataset_final)

        frequent_item_set = generate_frequent_item_set(first_candidate_set, nbr_trans, min_support, dataset_final, father_frequent_array)
        association_rules = generate_association_rule(father_frequent_array)
        output_apriori = apriori(association_rules, dataset_final, min_support, min_confidence)

        if len(output_apriori) == 0:
            st.warning("Il n'y a pas de règles d'associations pour ce support")
        else:
            st.markdown("<hr><h4 style='font-weight:bold;'>Règles d'association</h4>", unsafe_allow_html=True)
            output_apriori_gen = []
            for i in range(0, len(output_apriori), 5):
                l = []
                rule = output_apriori[i + 3]
                support_x = output_apriori[i]
                support_x_y = output_apriori[i + 1]
                confidence = output_apriori[i + 2]
                lift = output_apriori[i + 4]
                l.append(rule[0])
                l.append(rule[1])
                l.append(support_x)
                l.append(support_x_y)
                l.append(confidence)
                l.append(lift)
                output_apriori_gen.append(l)
                    
            dt = pd.DataFrame(output_apriori_gen, columns=["X", "Y", "Support de X en %", "Support de X & Y en %", "Niveau de Confiance %", "Lift"])
            st.dataframe(dt, width=1500)
            
            st.markdown("<hr><h4 style='font-weight:bold;'>Top 10 des recommandations les plus bénéfiques</h4>", unsafe_allow_html=True)
            
            top_10_recommendations = sorted(output_apriori_gen, key=lambda x: float(x[5]), reverse=True)[:10]

            dt3 = pd.DataFrame(top_10_recommendations, columns=["X", "Y", "Support de X en %", "Support de X & Y en %", "Niveau de Confiance %", "Lift"])
            st.dataframe(dt3, width=1500)
            
            st.markdown("<hr><hr>", unsafe_allow_html=True)
            st.markdown("<h4 style='font-weight:bold;'>Exécution de l'algotithme sur une plage du support</h4>", unsafe_allow_html=True)
            option = st.selectbox('Voulez-vous afficher le temps d\'exécution de l\'algo en fonction du support', ["Non", "Oui"])
            if option == "Oui":
                support_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                
                execution_times = []

                father_frequent_array2 = []
                for sup in support_values:
                    st.markdown(f"<hr><h4 style='font-weight:bold;'>Ensemble des éléments fréquents pour support = {sup} %</h4>", unsafe_allow_html=True)
                    start_time = time.time()
                    
                    frequent_item_set2 = generate_frequent_item_set(first_candidate_set, nbr_trans, sup, dataset_final, father_frequent_array2)
                    association_rules2 = generate_association_rule(father_frequent_array2)
                    output_apriori2 = apriori(association_rules2, dataset_final, sup, min_confidence)
                    
                    end_time = time.time()
                    execution_time = end_time - start_time
                    execution_times.append(execution_time)
                
                st.markdown("<hr><h4 style='font-weight:bold;'>Évolution du temps d'exécution en fonction du support</h4>", unsafe_allow_html=True)
                fig, ax = plt.subplots()
                plt.plot(support_values, execution_times, marker='o')
                plt.xlabel('Support (%)')
                plt.ylabel('Temps d\'exécution (s)')
                plt.title('Évolution du temps d\'exécution en fonction du support')
                plt.grid(True)
                st.pyplot(fig)

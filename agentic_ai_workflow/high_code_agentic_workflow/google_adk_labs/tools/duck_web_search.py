from ddgs import DDGS


class DuckWebSearch:
    
    def web_search(self, query:str)->str:
      
       
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
        except Exception as e:
            return [{"title":"Errore ricerca", "body":f"Ricerca fallita : {e}", "href":""}]
            

        if not results:
            return [{"title": "Nessun risultato", "body": "Nessun risultato trovato per questa query.", "href": ""}]
        
        search_results = []
        for r in results:
          
            search_results.append({
                "body": r.get('body', ''),
                "href":r.get('href', '')
            })
            
        print(f"SEARCH RESULTS {search_results}")
        return search_results
  
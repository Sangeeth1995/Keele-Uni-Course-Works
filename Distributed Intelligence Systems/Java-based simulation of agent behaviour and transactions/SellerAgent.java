import java.util.ArrayList;
import java.util.List;

public class SellerAgent extends Agent {
	private String targetBook;
	private int targetBookIndex;

	private ArrayList<Book> inventory = new ArrayList<Book>(); 
	
	public void receiveTender(String target){
		targetBook = target;
	}
    
    public String getTarget(){
    	return targetBook;
    }

    public void receiveBook(Book book){
		inventory.add(book);
	}

	//check whether title is in inventory. Return price if true, else return -1
	public float checkInventory(){
		float targetInventoryPrice = -1; // acts as boolean
		int i = 0;
		while (i < inventory.size()){

			
			if (targetBook.equalsIgnoreCase(inventory.get(i).getBk_name())){
				targetInventoryPrice = inventory.get(i).getBk_price();
				//Set targgetBookIndex if it needs to be selected
				targetBookIndex = i;
				//Break after first instance of book in inventory;
				break;
			}
		i++;
		}
		return targetInventoryPrice;
	}

	public Book buyBook(SellerAgent lowestPriceSeller){
		System.out.print(lowestPriceSeller.getAgentId()+" had "+ inventory.size()+ " items...");
		Book transferBook = inventory.get(targetBookIndex);
		inventory.remove(targetBookIndex);
		System.out.print("After sale there are "+ inventory.size()+ " items. Book transferred.");
		return transferBook;
	} 
}

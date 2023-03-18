
public class BuyerAgent extends Agent {
	private String targetBook;
	private SellerAgent lowestPriceSeller;
	private float lowestPrice;
	private Book bookHolder; // This will hold the target book if found.


	public void setTarget(String target){
		//The book the user wants to buy
		targetBook = target;
	}
	

	public void issueTender(SellerAgent targetAgent){
		targetAgent.receiveTender(targetBook);
	}

	public void searchAgent(SellerAgent targetAgent){
		//This function searches a seller agent whether they have book in inventory.
		//If so, this price is inserted into lowestPrice if there are no previous offers,
		//Or there is a comparison to check whether it is the lowest bid. 
		float targetPrice = targetAgent.checkInventory();
		if (targetPrice > 0){
			System.out.println(targetAgent.getAgentId() + " has book in stock at price "+
				Float.toString(targetPrice));
			// if no prices received, set this as lowest price and bidder
			if (lowestPriceSeller == null){
				lowestPriceSeller = targetAgent;
				lowestPrice = targetPrice;

			} else {
				//Check whether this price is lowest
				if(targetPrice < lowestPrice){
					lowestPriceSeller = targetAgent;
					lowestPrice = targetPrice;
				}
			}

		} else {
			System.out.println(targetAgent.getAgentId() + " does NOT have book in stock");
		}
	}

	public void reportResult(){
		if(lowestPriceSeller != null){
			System.out.println("The lowest price for " + targetBook+
			" is: " + Float.toString(lowestPrice) + ". The "+
			"bid was made by " + lowestPriceSeller.getAgentId());	
		}
		else{
			System.out.println("There were no bids.");
		}
		
	}

	public void transferBook(){
		if(lowestPriceSeller == null){
			System.out.println("The requested book is out of stock");
			
		}else {
		bookHolder = lowestPriceSeller.buyBook(lowestPriceSeller);
		}

	}

	public void reportBookTransfer(){
		if(lowestPriceSeller != null){
		System.out.println(bookHolder.getBk_name() + " was successfully "+
			"bought for " + Float.toString(bookHolder.getBk_price()));
	}
		}

}

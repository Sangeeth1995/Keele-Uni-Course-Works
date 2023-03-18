
public class Book {
	
	
	private String bk_name;
	private float bk_price;
	
	public Book(String bk_name) {
		this.bk_name = bk_name;
		int maxBookPrice = 1000;
		int minBookPrice = 100;
		int range = maxBookPrice - minBookPrice;
		this.bk_price = (int) (Math.random()*range) + minBookPrice;
	}
	
	
	public Book(String bk_name,float bk_price) {
		this.bk_name = bk_name;
		this.bk_price = bk_price;
	}
	public String getBk_name() {
		return bk_name;
	}

	public float getBk_price() {
		return bk_price;
	}
	
}

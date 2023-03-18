import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Collections;
import java.util.Random;
import java.util.Scanner;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;






public class BookTrade {


	public static void main(String[] args) throws IOException {
		
		
		
		//Creating an array for the initial catalogues 
		//We are generating randomly created titles for books
		String[] book_titles = new String[150];
		//generate titles for first 100 titles
		for (int i = 0; i < 100; i++){
			book_titles[i] = "book" + Integer.toString(i);
		}
		//Generating single duplicate numbers to replicate multiple copies of books
		final int[] duplicates = new Random().ints(1, 100).distinct().limit(50).toArray();

		//Adding these duplicates to the existing array
		for (int i = 1; i < duplicates.length; i++){
			book_titles[i+100] = "book" + Integer.toString(duplicates[i]);

		}

		//Creating an inventory array to add book objects
		Book[] bookInventory = new Book[book_titles.length];
		//For each book title we are generating a random price.
		for( int i = 0; i < book_titles.length; i++){
			Book book = new Book(book_titles[i]);
			bookInventory[i] = book;
		}
		
		//Creating 50 Seller agents
		SellerAgent[] sellers = new SellerAgent[50];

		
		for (int i = 0; i < sellers.length; i++){
			sellers[i] = new SellerAgent();
			sellers[i].setAgentId("seller_" + Integer.toString(i));
		}
		
		//Beginning
		
		while (true) {
			  
		
		System.out.println ("\nEnter the type of Agent you want to proceed with ?  (e.g. 1 for Buyer Agent and 2 for Seller Agent)?");
		System.out.println ("\n1.Buyer Agent \t 2.Seller Agent \t 3.Exit\n");
		Scanner sc = new Scanner(System.in);
		BufferedReader br = new BufferedReader(
	            new InputStreamReader(System.in));
		int agentType = sc.nextInt();
		if (agentType == 1) {
			

		//initializing buyer agent
		BuyerAgent buyerAg = new BuyerAgent();
		buyerAg.setAgentId("buyer1");

		//Checking the user to find the target book
		System.out.println ("\nInitially we have 100 books in the catelogue ie; book0 to book99");
		System.out.println ("\nEnter the book(title) you want to find (e.g. book1)?\n");
	    String bookTarget = br.readLine();

		Collections.shuffle(Arrays.asList(bookInventory));

		//distributing books object to the seller agents
		int count = 0;
		while (count < bookInventory.length){
			for (int i = 0; i < sellers.length; i++){
				sellers[i].receiveBook(bookInventory[count]);
				count++;
			}
		}

		

		buyerAg.setTarget(bookTarget);
		System.out.println ("Issuing bid for Book "+bookTarget+".");
		
		//issuing tenders to all seller agents
		for (int i = 0; i < sellers.length; i++){
			buyerAg.issueTender(sellers[i]);
		}


		//issue tenders to all seller agents
		for (int i = 0; i < sellers.length; i++){
			sellers[i].getAgentId();
			buyerAg.searchAgent(sellers[i]);
			buyerAg.reportResult();
		}

		//Transfer book and report result
		buyerAg.transferBook();
		buyerAg.reportBookTransfer();
		
		
		}else if (agentType == 2) {
			
		      JFrame frame = new JFrame("Seller Agent GUI");
		       frame.setSize(1000,150);

		       frame.setVisible(true);
		        //Creating the panel at bottom and adding components
		        JPanel panel = new JPanel(); // the panel is not visible in output
		        JLabel s_id = new JLabel("Enter Seller ID(0-49):");
		        JTextField s_tf = new JTextField(10); // accepts upto 10 characters
		        JLabel bt = new JLabel("Enter the book title:");
		        JTextField bt_tf = new JTextField(20); // accepts upto 20 characters
		        JLabel bp = new JLabel("Enter the book price:");
		        JTextField bp_tf = new JTextField(10); // accepts upto 10 characters
		        
		        JButton Add = new JButton("Add");
		        
		        // Components Added
		        panel.add(s_id); 
		        panel.add(s_tf);
		        panel.add(bt); 
		        panel.add(bt_tf);
		        panel.add(bp); 
		        panel.add(bp_tf);
		        panel.add(Add);

		        
		        
		        Add.addActionListener(new ActionListener(){
					public void actionPerformed(ActionEvent ev) {
						
							int sid = Integer.parseInt(s_tf.getText().trim());
							String bk_name = bt_tf.getText().trim();
							float bk_price = Float.parseFloat(bp_tf.getText().trim());
							Book book1 = new Book(bk_name,bk_price);
							if (sid > 49) {
								System.out.print("Invalid Seller Agent ID.\n");
								System.out.println("Press Enter to continue");
								frame.dispose();
								} else {
									
									sellers[sid].receiveBook(book1);
									System.out.print("Added book data to the "+ sellers[sid].getAgentId()+"\n");
									System.out.println("Press Enter to continue");

									frame.dispose();								}
							
	
							

			
					}
				} );
		        

		        //Adding Components to the frame.
		        frame.getContentPane().add(BorderLayout.NORTH, panel);
		        frame.getContentPane().add(BorderLayout.SOUTH, Add);
		        frame.setVisible(true);
		        
		        br.readLine();			

//			We can also use below code snippet to implement seller agent flow without GUI
//			System.out.print("Choose the seller agent(0-49) :");
//			int sid = sc.nextInt();
//			System.out.print("Enter the book name : ");
//			String bk_name = br.readLine();
//			System.out.print("Enter the book price : ");
//			int bk_price = sc.nextInt();
//			Book book1 = new Book(bk_name,bk_price);
//			sellers[sid].receiveBook(book1);
//			System.out.print("Added book date to the"+ sellers[sid].getAgentId());

		}else if (agentType == 3) {
			System.exit(0);
		}else {
				System.out.println ("Invalid Agent type! \n");
			  
			}
		}


	}




}
	

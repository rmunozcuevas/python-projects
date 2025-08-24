import java.util.Scanner;

class Shirt {
    int quantity;
    String brand;
    String clothe_type;

    public Shirt(int quantity, String brand, String clothe_type) {
        this.quantity = quantity;
        this.brand = brand;
        this.clothe_type = clothe_type;
    }
}

class Pants extends Shirt {

    public Pants(int quantity, String brand, String clothe_type) {
        super(quantity, brand, clothe_type);
    }

    // for choice() implement an input where you choose the quantity and brand

    public String choice(int quantity, String brand, String clothe_type){
        return "You have chosen: " + quantity + "of "  + brand + "for your " + clothe_type;

    }

}

class Shoes extends Shirt {
    int shoeSize;

    public Shoes(int quantity, String brand, String clothe_type, int shoeSize) {
        super(quantity, brand, clothe_type); // calls Shirt constructor
        this.shoeSize = shoeSize;
    }

    public static String Size(int quantity, int shoeSize, String brand){
        System.out.print("");
    }
}

class Outerwear extends Shirt {
    String Outertype;
    public Outerwear(int quantity, String brand, String clothe_type, String Outertype){
        super(quantity, brand, clothe_type);
        this.Outertype = Outertype;
    }

}






public class Main {
    public static int[] QuickSort(int[] array){

    }
    
    public static String Common_Types(String choose){
        Scanner scanner = new Scanner(System.in);
    
        System.out.print("Enter the type of brand you want to categorize: ");
        String name = scanner.nextLine();
    
        while(!name.matches("[a-zA-Z ]+")){
            System.out.println("Please enter a valid brand!");
            name = scanner.nextLine();
        }
    
        scanner.close();
    
        return name;
        
    
    }


    public static void main(String[] args){



    }
}

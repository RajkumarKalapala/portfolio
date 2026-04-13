public class Demo {
    public static void main(String[] args) {
        // Test BankAccount
        BankAccount acc = new BankAccount("20120", "John Doe");
        acc.deposit(500);
        acc.deposit(1500);
        System.out.println("Balance: " + acc.getBalance()); // 2000

        // Test SavingsAccount
        SavingsAccount saving = new SavingsAccount("20121", "Jane Doe", 10);
        saving.deposit(500);
        System.out.println("Before interest: " + saving.getBalance());
        saving.addInterest();
        System.out.println("After interest: " + saving.getBalance());

        // Test CheckingAccount
        CheckingAccount checking = new CheckingAccount("20122", "Bob Smith");
        checking.deposit(500);
        checking.withdraw(200);
        checking.deposit(700);
        checking.deductFees();
        System.out.println("Checking balance: " + checking.getBalance());
    }
}

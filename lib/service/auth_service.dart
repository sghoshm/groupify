import 'package:firebase_auth/firebase_auth.dart';
import 'package:groupify/helper/helper_function.dart';
import 'package:groupify/service/database_service.dart';

class AuthService {
  FirebaseAuth firebaseAuth = FirebaseAuth.instance;
  //Login Function
  Future loginWithUserNameAndPassword(String email, String password) async {
    try {
      User user = (await firebaseAuth.signInWithEmailAndPassword(
              email: email, password: password))
          .user!;
      if (user != null) {
        return true;
      }
    } on FirebaseAuthException catch (e) {
      return e.message;
    }
  }

  //Register Function
  Future registerUserWithEmailAndPassword(String fullName, String email,
      String password, String phoneNumber, String countryCode) async {
    try {
      User user = (await firebaseAuth.createUserWithEmailAndPassword(
              email: email, password: password))
          .user!;
      if (user != null) {
        await DatabaseService(uid: user.uid)
            .savingUserData(fullName, email, phoneNumber, countryCode);
        return true;
      }
    } on FirebaseAuthException catch (e) {
      return e.message;
    }
  }

  //SignOut Function
  Future signOut() async {
    try {
      await HelperFunctions.saveUserLoggedInStatus(false);
      await HelperFunctions.saveUserNameSF("");
      await HelperFunctions.saveUserEmailSF("");
      await HelperFunctions.saveUserPhoneNumberSF("");
      await HelperFunctions.saveUserCountryCodeSF("");
      await firebaseAuth.signOut();
    } catch (e) {
      return null;
    }
  }
}

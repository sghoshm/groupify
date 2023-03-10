import 'package:shared_preferences/shared_preferences.dart';

class HelperFunctions {
  static String userLoggedInKey = "USERLOGGEDINKEY";
  static String userNameKey = "USERNAMEKEY";
  static String userEmailKey = "USEREMAILKEY";
  static String userPhoneNumberKey = "USERPHONENUMBERKEY";
  static String userCountryCodeKey = "USERCOUNTRYCODEKEY";
  //save data to shared preferences
  static Future<bool> saveUserLoggedInStatus(bool isUserLoggedIn) async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return sf.setBool(userLoggedInKey, isUserLoggedIn);
  }

  static Future<bool> saveUserNameSF(String userName) async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return await sf.setString(userNameKey, userName);
  }

  static Future<bool> saveUserEmailSF(String userEmail) async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return await sf.setString(userEmailKey, userEmail);
  }

  static Future<bool> saveUserPhoneNumberSF(String userPhoneNumber) async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return await sf.setString(userPhoneNumberKey, userPhoneNumber);
  }

  static Future<bool> saveUserCountryCodeSF(String userCountryCode) async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return await sf.setString(userCountryCodeKey, userCountryCode);
  }

  //get data from shared preferences
  static Future<bool?> getUserLoggedInStatus() async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return sf.getBool(userLoggedInKey);
  }

  static Future<String?> getUserEmailFromSF() async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return sf.getString(userEmailKey);
  }

  static Future<String?> getUserNameFromSF() async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return sf.getString(userNameKey);
  }

  static Future<String?> getPhoneNumberFromSF() async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return sf.getString(userPhoneNumberKey);
  }

  static Future<String?> getCountryCodeFromSF() async {
    SharedPreferences sf = await SharedPreferences.getInstance();
    return sf.getString(userCountryCodeKey);
  }
}

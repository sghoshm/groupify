import 'package:flutter/material.dart';
import 'package:groupify/pages/auth/login_page.dart';
import 'package:groupify/pages/search_page.dart';
import 'package:groupify/service/auth_service.dart';
import 'package:groupify/widgets/widgets.dart';

import '../helper/helper_function.dart';
import 'profile_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String userName = "";
  String email = "";
  String phoneNumber = "";
  @override
  void initState() {
    super.initState();
    gettingUserData();
  }

  gettingUserData() async {
    await HelperFunctions.getUserNameFromSF().then((value) {
      setState(() {
        userName = value!;
      });
    });
    await HelperFunctions.getUserEmailFromSF().then((value) {
      setState(() {
        email = value!;
      });
    });
    await HelperFunctions.getPhoneNumberFromSF().then((value) {
      setState(() {
        phoneNumber = value!;
      });
    });
  }

  AuthService authService = AuthService();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          actions: [
            IconButton(
                onPressed: () {
                  nextScreen(context, const SearchPage());
                },
                icon: Icon(Icons.search))
          ],
          elevation: 2,
          centerTitle: true,
          backgroundColor: Theme.of(context).primaryColor,
          title: const Text(
            "Groups",
            style: TextStyle(
              fontWeight: FontWeight.w700,
              fontSize: 27,
            ),
          ),
        ),
        drawer: Drawer(
          child: ListView(
            padding: const EdgeInsets.symmetric(vertical: 50),
            children: <Widget>[
              Icon(
                Icons.account_circle_sharp,
                size: 150,
                color: Theme.of(context).primaryColor,
              ),
              const SizedBox(
                height: 20,
              ),
              Text(userName,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                      fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(
                height: 30,
              ),
              const Divider(
                height: 2,
              ),
              ListTile(
                onTap: () {},
                selectedColor: Theme.of(context).primaryColor,
                selected: true,
                contentPadding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 5),
                leading: const Icon(Icons.group),
                title: const Text("Groups",
                    style: TextStyle(
                      color: Colors.black,
                    )),
              ),
              ListTile(
                onTap: () {
                  nextScreenReplace(
                      context,
                      ProfilePage(
                        userName: userName,
                        email: email,
                        phoneNumber: phoneNumber,
                      ));
                },
                contentPadding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 5),
                leading: const Icon(Icons.account_box),
                title: const Text("Profile",
                    style: TextStyle(
                      color: Colors.black,
                    )),
              ),
              ListTile(
                onTap: () async {
                  showDialog(
                    barrierDismissible: false,
                    context: context,
                    builder: (context) {
                      return AlertDialog(
                        title: const Text("Logout"),
                        content: const Text("Are you sure you want to logout?"),
                        actions: [
                          IconButton(
                            onPressed: () {
                              Navigator.pop(context);
                            },
                            icon: const Icon(
                              Icons.cancel_outlined,
                              color: Colors.red,
                            ),
                          ),
                          IconButton(
                            onPressed: () async {
                              await authService.signOut();
                              Navigator.of(context).pushAndRemoveUntil(
                                  MaterialPageRoute(
                                      builder: (context) => const LoginPage()),
                                  (route) => false);
                            },
                            icon: const Icon(
                              Icons.done_all_outlined,
                              color: Colors.green,
                            ),
                          ),
                        ],
                      );
                    },
                  );
                },
                contentPadding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 5),
                leading: const Icon(Icons.logout),
                title: const Text("Logout",
                    style: TextStyle(
                      color: Colors.black,
                    )),
              ),
            ],
          ),
        ),
        body: groupList(),
        floatingActionButton: FloatingActionButton(
          onPressed: () {
            popUpDialog(context);
          },
          backgroundColor: Theme.of(context).primaryColor,
          child: const Icon(Icons.add),
        ));
  }

  popUpDialog(BuildContext context) {
    return showDialog(
        context: context,
        builder: (context) {
          return AlertDialog(
            title: const Text("Create Group"),
            content: const TextField(
              decoration: InputDecoration(
                hintText: "Enter Group Name",
              ),
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                child: const Text("Cancel"),
              ),
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                child: const Text("Create"),
              ),
            ],
          );
        });
  }

  groupList() {}
}

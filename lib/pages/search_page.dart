import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:groupify/helper/helper_function.dart';
import 'package:groupify/service/database_service.dart';
import 'package:groupify/widgets/widgets.dart';

import '../widgets/group_tile.dart';
import 'chat_page.dart';
import 'home_page.dart';

class SearchPage extends StatefulWidget {
  const SearchPage({Key? key}) : super(key: key);

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  static TextEditingController searchController = TextEditingController();
  bool isLoading = false;
  bool isJoined = false;
  QuerySnapshot? searchSnapshot;
  bool hasUserSearched = false;
  String userName = "";
  User? user;
  @override
  void initState() {
    getCurrentUserIdAndName();
    super.initState();
  }

  getCurrentUserIdAndName() async {
    await HelperFunctions.getUserNameFromSF().then((value) {
      setState(() {
        userName = value!;
      });
    });
    user = FirebaseAuth.instance.currentUser;
  }

  String getName(String r) {
    return r.substring(r.indexOf("_") + 1);
  }

  String getId(String res) {
    return res.substring(0, res.indexOf("_"));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text(
            "Search",
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 27),
          ),
          centerTitle: true,
          elevation: 0,
          backgroundColor: Theme.of(context).primaryColor,
        ),
        body: Column(
          children: [
            Container(
              color: Theme.of(context).primaryColor.withOpacity(0.2),
              padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 10),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: searchController,
                      style: const TextStyle(
                        color: Colors.black,
                        fontSize: 20,
                      ),
                      decoration: const InputDecoration(
                        border: InputBorder.none,
                        hintStyle: TextStyle(color: Colors.black, fontSize: 16),
                        hintText: "Search Groups...",
                      ),
                    ),
                  ),
                  GestureDetector(
                    onTap: () {
                      initiateSearchMethod();
                    },
                    child: Container(
                      width: 40,
                      height: 40,
                      decoration: BoxDecoration(
                        color: Theme.of(context).primaryColor.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(50),
                      ),
                      child: const Icon(
                        Icons.search,
                        color: Colors.black,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            isLoading
                ? Center(
                    // ignore: sort_child_properties_last
                    child: CircularProgressIndicator(
                      color: Theme.of(context).primaryColor,
                    ),
                  )
                : groupList(),
          ],
        ));
  }

  initiateSearchMethod() async {
    if (searchController.text.isNotEmpty) {
      setState(() {
        isLoading = true;
      });
      await DatabaseService()
          .searchByName(searchController.text)
          .then((snapshot) {
        setState(() {
          searchSnapshot = snapshot;
          isLoading = false;
          hasUserSearched = true;
        });
      });
    }
  }

  groupList() {
    return hasUserSearched
        ? ListView.builder(
            shrinkWrap: true,
            itemCount: searchSnapshot!.docs.length,
            itemBuilder: (context, index) {
              return groupTile(
                userName,
                searchSnapshot!.docs[index]["groupId"],
                searchSnapshot!.docs[index]["groupName"],
                searchSnapshot!.docs[index]["admin"],
              );
            },
          )
        : Container();
  }

  joinedOrNot(
      String userName, String groupId, String groupName, String admin) async {
    await DatabaseService(uid: user!.uid)
        .isUserJoined(groupName, groupId, userName)
        .then((value) {
      setState(() {
        isJoined = value;
      });
    });
  }

  Widget groupTile(
      String userName, String groupId, String groupName, String admin) {
    //function to check if user already in group
    joinedOrNot(userName, groupId, groupName, admin);
    return ListTile(
      contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      leading: CircleAvatar(
        backgroundColor: Theme.of(context).primaryColor,
        child: Text(groupName.substring(0, 1).toUpperCase()),
      ),
      title: Text(
        groupName,
        style: const TextStyle(
          color: Colors.black,
          fontSize: 20,
          fontWeight: FontWeight.w600,
        ),
      ),
      subtitle: Text(
        "Admin: ${getName(admin)}",
        style: const TextStyle(
          color: Colors.black,
          fontSize: 15,
        ),
      ),
      trailing: InkWell(
          onTap: () async {
            await DatabaseService(uid: user!.uid)
                .toggleGroupJoin(groupName, groupId, userName);
            if (isJoined) {
              setState(() {
                isJoined = !isJoined;
              });
              // ignore: use_build_context_synchronously
              showSnackbar(context, Color.fromARGB(255, 1, 137, 71),
                  "Sucessfully Joined $groupName");
              Future.delayed(const Duration(seconds: 1), () {
                nextScreen(
                  context,
                  ChatPage(
                    groupId: groupId,
                    groupName: groupName,
                    userName: userName,
                  ),
                );
              });
            } else {
              setState(() {
                isJoined = !isJoined;
                showSnackbar(
                    context, Colors.redAccent, "Left the Group $groupName");
                nextScreen(context, const HomePage());
              });
            }
          },
          child: isJoined
              ? Container(
                  decoration: BoxDecoration(
                      color: Colors.black,
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: Colors.white, width: 1)),
                  padding:
                      const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  child: const Text(
                    "Joined",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 15,
                    ),
                  ),
                )
              : Container(
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      color: Theme.of(context).primaryColor),
                  padding:
                      const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  child: const Text(
                    "Join",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 15,
                    ),
                  ),
                )),
    );
  }
}
